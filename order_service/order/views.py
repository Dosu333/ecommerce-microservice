from django.db.models import Exists, OuterRef
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permissions import IsCustomer, IsVendor
from .models import Order
from .serializers import OrderSerializer, ListOrderSerializer
from core.exceptions import CustomValidationError
from core.grpc import check_product_availability


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    http_method_names = ['get', 'post']
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated] 
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, (IsCustomer | IsVendor)]
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
        context["request_user"] = self.request.user
        return context
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'status': response.status_code,
            'message': 'Order has been created successfully',
            'data': response.data,
        }
        return response
