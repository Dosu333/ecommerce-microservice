from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.database import products_collection
from core.celery import APP
from core.utils import upload_images
import cloudinary
import logging

logger = logging.getLogger(__name__)

@APP.task
def upload_product_image_to_cloudinary(image_data, product_id):
    try:
        upload_result = cloudinary.uploader.upload(image_data)
        image_url = upload_result['secure_url']

        # Update MongoDB with the new image URL
        products_collection.update_one(
            {"id": product_id},
            {"$push": {"images": image_url}}
        )

        # Send a WebSocket event to notify the client
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'product_{product_id}',
            {
                "type": "send_image_update",
                "image_url": image_url,
            }
        )

        return image_url
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return None  

@APP.task   
def update_category_name(category_id, new_name):
    """Update category_name in all products that belong to this category."""
    products_collection.update_many(
        {"category_id": category_id},  # Find all products with this category_id
        {"$set": {"category_name": new_name}}  # Update category_name
    )
