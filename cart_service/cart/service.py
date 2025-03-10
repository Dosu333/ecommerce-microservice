import json
from django.core.cache import cache
from .models import Cart, CartItem

class CartService:
    CART_KEY = "cart:{user_id}"

    @staticmethod
    def get_cart(user_id):
        """Fetch the cart from Redis or create an empty cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart_data = cache.get(key)
        if cart_data is None:
            return {}
        return json.loads(cart_data)

    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        """Add a product to the Redis cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart = CartService.get_cart(user_id)

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        cache.set(key, json.dumps(cart), timeout=3600)  # Expires in 1 hour
        return cart

    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove a product from the Redis cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart = CartService.get_cart(user_id)

        if product_id in cart:
            del cart[product_id]

        cache.set(key, json.dumps(cart), timeout=3600)
        return cart

    @staticmethod
    def persist_cart(user_id):
        """Move cart data from Redis to PostgreSQL."""
        cart_data = CartService.get_cart(user_id)
        if not cart_data:
            return None  # No cart to save

        cart, created = Cart.objects.get_or_create(user_id=user_id)

        for product_id, quantity in cart_data.items():
            CartItem.objects.update_or_create(
                cart=cart,
                product_id=product_id,
                defaults={"quantity": quantity},
            )

        cache.delete(CartService.CART_KEY.format(user_id=user_id))  # Clear Redis cart
        return cart
