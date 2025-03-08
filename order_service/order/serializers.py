from rest_framework import serializers
from core.grpc import get_product_detail, check_product_availability
from core.exceptions import CustomValidationError
from .models import Order


class OrderItemSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity", "unit_price"]
        
    def get_product_data(self, obj):
        product = get_product_detail(str(obj.product_id))
        return {
            "name": product.name,
            "slug": product.slug
        }
        

class OrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True, error_messages={"required": "Address field is required."})
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user_id", "status", "total_price", "items", "created_at"]

    def create(self, validated_data):
        """Create an order with multiple products"""
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        
        for item in items_data:
            product_response = check_product_availability(item['product_id'], item['quantity'])
            if not product_response.available:
                product_detail = get_product_detail(item['product_id'])
                raise CustomValidationError(f"{product_detail.name} is out of stock")
            continue

        order_items = [
            OrderItem(order=order, **item_data) for item_data in items_data
        ]
        OrderItem.objects.bulk_create(order_items)

        # Update total price
        order.update_total_price()
        return order

