from django.db.models import Exists, OuterRef
from rest_framework import views, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decouple import config
from core.permissions import IsCustomer, IsVendor
from core.exceptions import CustomValidationError, CustomInternalServerError
from core.grpc import check_product_availability
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer, RetrieveOrderSerializer, UpdateOrderSerializer
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
    http_method_names = ['get', 'post', 'patch']
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated] 
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['partial_update', 'update']:
            permission_classes = [IsAuthenticated, (IsCustomer | IsVendor)]
        else:
            permission_classes = [IsAuthenticated, IsCustomer]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'retrieve':
            return RetrieveOrderSerializer
        elif self.action in ['partial_update', 'update']:
            return UpdateOrderSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        is_vendor = IsVendor().has_permission(self.request, self)
        user = self.request.user

        if is_vendor:
            return self.queryset.filter(vendor_id=user.id)
        return self.queryset.filter(user_id=user.id)
    
    def perform_create(self, serializer):
        order = serializer.save(user_id=self.request.user.id)
        payment = initialize_payment(self.request.headers, str(order.id), float(order.total_price), str(order.vendor_id))
        
        if payment['success']:
            order.payment_link = payment['payment_link']
            order.save()
        else:
            if payment["message"]:
                raise CustomInternalServerError(payment['message'])
            raise CustomInternalServerError("Payment intialization failed")
        
    def perform_update(self, serializer):
        data = serializer.validated_data
        is_vendor = IsVendor().has_permission(self.request, self)
        is_customer = IsVendor().has_permission(self.request, self)
        if is_vendor and data['status'] != 'cancelled':
            raise CustomValidationError("You can only cancel an order")
        elif is_customer and data['status'] != "delivered":
            raise CustomValidationError("You can only mark your order as delivered")
        order = serializer.save()
        if data['status'] == "cancelled":
             redis_client.xadd("order_stream", {"event": "order_cancelled", "order_id": str(order.id)})
        elif data["status"] == "completed":
            redis_client.xadd("order_stream", {"event": "order_delivered", "order_id": str(order.id)})
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        clear_cart.apply_async((request.headers.get("Authorization"), ))
        response.data = {
            'status': response.status_code,
            'message': 'Order has been created successfully',
            'data': response.data,
        }
        return response
    
class RetryPaymentView(views.APIView):
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
