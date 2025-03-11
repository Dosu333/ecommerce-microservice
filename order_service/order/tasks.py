from decouple import config
from core.celery import APP
import requests
import logging

logger = logging.getLogger(__name__)
CART_SERVICE_URL = config("CART_SERVICE_URL")

@APP.task
def clear_cart(auth_header):
    try:
        url = f"{CART_SERVICE_URL}/cart/clear/"
        headers = {"Authorization": auth_header}
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        logger.error(f"Error clearing cart: {e}")
        return None  
        