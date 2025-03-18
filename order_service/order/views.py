from django.db.models import Exists, OuterRef
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decouple import config
from core.permissions import IsCustomer, IsVendor
from core.exceptions import CustomValidationError, CustomInternalServerError
from core.grpc import check_product_availability
from .models import Order
from .serializers import OrderSerializer, ListOrderSerializer
from .utils import initialize_payment
from .tasks import clear_cart
import redis


host = config("REDIS_HOST")
port = config("REDIS_PORT")
redis_client = redis.Redis(host=host, port=port, decode_responses=True)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    http_method_names = ['get', 'post']
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated] 
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsCustomer]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ListOrderSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        is_vendor = IsVendor().has_permission(self.request, self)
        user = self.request.user

        if is_vendor:
            # Filter orders where at least one order item belongs to the vendor
            return self.queryset.filter(
                Exists(OrderItem.objects.filter(order=OuterRef("id"), vendor_id=user.id))
            )
        
        return self.queryset.filter(user_id=user.id)

    def get_serializer_context(self):
        """Pass the request user to the serializer to filter order items."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    
    def perform_create(self, serializer):
        order = serializer.save(user_id=self.request.user.id)
        payment = initialize_payment(self.request.headers, str(order.id), float(order.total_price))
        
        if payment['success']:
            order.payment_link = payment['payment_link']
        else:
            if payment["message"]:
                raise CustomInternalServerError(payment['message'])
            raise CustomInternalServerError("Payment intialization failed")
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        clear_cart.apply_async((request.headers.get("Authorization"), ))
        response.data = {
            'status': response.status_code,
            'message': 'Order has been created successfully',
            'data': response.data,
        }
        return response
    
class RetryPaymentView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            if order.is_paid:
                return Response({"status": 400, "error": "Order has been paid for already"}, status=status.HTTP_400_BAD_REQUEST)
            payment = initialize_payment(request.headers, order_id, float(order.total_price))
            
            if payment['success']:
                return Response({"status": 200, "message": "New payment link generated", "data": {"payment_link": payment['payment_link']}}, status=status.HTTP_200_OK)
            return Response({"status": 400, "error": "Failed to reinitialize payment"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"status": 404, "error": "Invalid order"}, status=status.HTTP_404_NOT_FOUND)
