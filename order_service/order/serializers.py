from rest_framework import serializers
from core.grpc import get_product_detail, check_product_availability
from core.exceptions import CustomValidationError
from core.permissions import IsVendor
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity", "unit_price", "product_data"]
        
    def get_product_data(self, obj):
        product = check_product_availability(str(obj.product_id), obj.quantity)
        return {
            "name": product.name,
            "slug": product.slug,
            "is_available": product.available
        }
        

class OrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True, error_messages={"required": "Address field is required."})
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user_id", "address", "status", "total_price", "payment_link", "items", "is_paid", "created_at"]

    def create(self, validated_data):
        """Create an order with multiple products"""
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        order_items = []
        
        for item_data in items_data:
            product_response = check_product_availability(str(item_data['product_id']), item_data['quantity'])
            if not product_response.available:
                if product_response.name:
                    raise CustomValidationError(f"{product_response.name} is out of stock")
                raise CustomValidationError("Product does not exist")
            order_items.append(OrderItem(order=order, vendor_id=product_response.vendor, unit_price=float(product_response.price), **item_data))
        OrderItem.objects.bulk_create(order_items)
        order.update_total_price()
        return order
    

class ListOrderSerializer(OrderSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        """Filter order items so vendors only see their items"""
        request = self.context.get("request")
        
        if request and IsVendor().has_permission(request, None):
            # Filter order items for vendor
            order_items = obj.items.filter(vendor_id=request.user.id)
        else:
            # Return all items for customers
            order_items = obj.items.all()

        return OrderItemSerializer(order_items, many=True).data

