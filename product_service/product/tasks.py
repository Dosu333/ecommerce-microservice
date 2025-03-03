from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.database import products_collection
from core.celery import APP
from core.utils import upload_images
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

@APP.task
def upload_product_image_to_cloudinary(images_data, product_id):
    try:
        image_urls = upload_images(images_data)

        # Update MongoDB with the new images
        products_collection.update_one(
            {"id": product_id},
            {"$push": {"images": image_urls}}
        )

        # Send a WebSocket event to notify the client
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'product_{product_id}',
            {
                "type": "send_image_update",
                "image_url": image_urls,
            }
        )

        return image_urls
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return None  
