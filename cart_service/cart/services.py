import json
from django.core.cache import cache
from .models import Cart, CartItem
from .serializers import CartSerializer

class CartService:
    CART_KEY = "cart:{user_id}"

    @staticmethod
    def get_cart(user_id):
        """Fetch the cart from Redis or create an empty cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart_data = cache.get(key)
        return CartSerializer(cart_data).data

    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        """Add a product to the Redis cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart = CartService.get_cart(user_id)
        cart_items = cart.get("items", [])

        for item in cart_items:
            if item.get("product_id") == product_id:
                item["quantity"] = quantity
                break
        else:
            cart_items.append({"product_id": product_id, "quantity": quantity})
        cart["items"] = cart_items
        serializer = CartSerializer(cart)
        cache.set(key, serializer.data, timeout=3600)  # Expires in 1 hour
        return serializer.data

    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove a product from the Redis cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart = CartService.get_cart(user_id)
        cart_items = cart.get("items", [])

        cart_items = [item for item in cart_items if item.get("product_id") != product_id]
        cart["items"] = cart_items

        serializer = CartSerializer(cart)
        cache.set(key, serializer.data, timeout=3600)  # Expires in 1 hour
        return serializer.data

    @staticmethod
    def persist_cart(user_id):
        """Move cart data from Redis to PostgreSQL."""
        cart_data = CartService.get_cart(user_id)
        if not cart_data:
            return None  # No cart to save

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        for item in cart_data.get("items", []):
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            CartItem.objects.update_or_create(
                cart=cart,
                product_id=product_id,
                defaults={"quantity": quantity},
            )

        cache.delete(CartService.CART_KEY.format(user_id=user_id))  # Clear Redis cart
        return cart
