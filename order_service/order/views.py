from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permissions import IsCustomer
from .models import Order
from .serializers import OrderSerializer
from core.exceptions import CustomValidationError
from core.grpc import check_product_availability


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        product_id = self.request.data.get("product_id")
        quantity = serializer.validated_data['quantity']
        
        if not product_id:
            Response({'status': 400, "message": "Invalid request. Product is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        product_response = check_product_availability(product_id, quantity)

        if not product_response.available:
            raise CustomValidationError("Product is out of stock!")
        total_price = float(product_response.price) * float(quantity)
        serializer.save(user_id=self.request.user.id, total_price=total_price)
