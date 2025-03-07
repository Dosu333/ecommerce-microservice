import grpc
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permissions import IsCustomer
from .models import Order
from .serializers import OrderSerializer
from decouple import config
import product_pb2
import product_pb2_grpc

PRODUCT_SERVICE_GRPC = config("PRODUCT_SERVICE_GRPC")

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

        # Connect to gRPC Product Service
        channel = grpc.insecure_channel(PRODUCT_SERVICE_GRPC)
        stub = product_pb2_grpc.ProductServiceStub(channel)
        product_request = product_pb2.ProductRequest(id=product_id, quantity=quantity)
        product_response = stub.CheckStock(product_request)

        if not product_response.available:
            raise serializers.ValidationError("Product is out of stock!")
        total_price = float(product_response.price) * float(quantity)
        serializer.save(user_id=self.request.user.id, total_price=total_price)
