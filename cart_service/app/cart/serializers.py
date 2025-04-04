from rest_framework import serializers
from core.grpc import check_product_availability
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity', "product_data"]
        
    def get_product_data(self, obj):
        try:
            product_id = str(obj.product_id)
            quantity = obj.quantity
        except:
            product_id = obj['product_id']
            quantity = obj['quantity']
        product = check_product_availability(product_id, quantity)
        return {
            "name": product.name,
            "slug": product.slug,
            "is_available": product.available
        }
        
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ["id", "items"]