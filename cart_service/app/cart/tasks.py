from django.core.cache import cache
from django.utils.timezone import now, timedelta
from decouple import config
from core.celery import APP
from .services import CartService
import json
import redis

host = config("REDIS_HOST")
port = config("REDIS_PORT")
redis_client = redis.StrictRedis(host=host, port=port, db=0)

@APP.task
def track_abandoned_carts():
    """Move carts older than 24 hours to PostgreSQL"""
    cutoff_time = (now() - timedelta(hours=24)).timestamp()
    carts = []

    # Get all carts that were last updated more than 24 hours ago
    expired_users = redis_client.zrangebyscore("abandoned_carts", "-inf", cutoff_time)

    for user_id in expired_users:
        user_id  = user_id.decode()
        key = f"cart:{user_id}"
        cart_data = cache.get(key)

        if cart_data:
            cart = CartService.persist_cart(user_id)
            redis_client.zrem("abandoned_carts", user_id)
            carts.append(str(cart.id))
    return carts
            

