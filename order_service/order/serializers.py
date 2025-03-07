from rest_framework import serializers
from core.grpc import get_product_detail
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True, error_messages={"required": "Address field is required."})
    product_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = "__all__"
        
    def get_product_data(self, obj):
        product = get_product_detail(str(obj.product_id))
        return {
            "name": product.name,
            "slug": product.slug,
            "price": product.price
        }
