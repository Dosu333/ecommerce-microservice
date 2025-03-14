import json
from django.core.cache import cache
from django.utils.timezone import now
from decouple import config
from .models import CartItem, Cart
from .serializers import CartSerializer
import redis
import time

host = config("REDIS_HOST")
port = config("REDIS_PORT")
redis_client = redis.StrictRedis(host=host, port=port, db=0)

class CartService:
    CART_KEY = "cart:{user_id}"

    @staticmethod
    def get_cart(user_id):
        """Fetch the cart from Redis or create an empty cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart_data = cache.get(key) or {"items": []}
        return CartSerializer(cart_data).data

    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        """Add a product to the Redis cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart = CartService.get_cart(user_id)
        cart_items = cart.get("items", [])

        updated = False
        for item in cart_items:
            if item["product_id"] == product_id:
                item["quantity"] = quantity
                updated = True
                break

        if not updated:
            cart_items.append({"product_id": product_id, "quantity": quantity})

        cart["items"] = cart_items
        timestamp = time.time()
        serializer = CartSerializer(cart)
        cache.set(key, serializer.data, timeout=96000)
        
        # Add timestamp to sorted set (float timestamp)
        redis_client.zadd("abandoned_carts", {str(user_id): timestamp})
        return serializer.data
    
    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove a product from the Redis cart."""
        key = CartService.CART_KEY.format(user_id=user_id)
        cart = CartService.get_cart(user_id)
        cart_items = [item for item in cart.get("items", []) if item["product_id"] != product_id]

        if not cart_items:  
            cache.delete(key)  # Delete cart if empty
            return cart

        cart["items"] = cart_items
        cache.set(key, CartSerializer(cart).data)
        return cart

    @staticmethod
    def persist_cart(user_id):
        """Move cart data from Redis to PostgreSQL."""
        cart_data = CartService.get_cart(user_id)
        if not cart_data or not cart_data.get("items"): 
            return None  

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        for item in cart_data["items"]:
            CartItem.objects.update_or_create(
                cart=cart,
                product_id=item["product_id"],
                defaults={"quantity": item["quantity"]},
            )

        cache.delete(CartService.CART_KEY.format(user_id=user_id))  # Clear Redis cart
        return cart
    
    @staticmethod
    def clear_cart(user_id):
        key = CartService.CART_KEY.format(user_id=user_id)
        cache.delete(key)
        redis_client.zrem("abandoned_carts", str(user_id))