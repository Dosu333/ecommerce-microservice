import pytest
import json
import uuid
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from product.consumers import ProductConsumer
from django.test import override_settings

@pytest.mark.asyncio
@override_settings(CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}})
async def test_websocket_product_updates():
    """Test WebSocket connection and image update event."""
    product_id = str(uuid.uuid4())
    
    communicator = WebsocketCommunicator(
        ProductConsumer.as_asgi(),
        path=f"/ws/products/{product_id}/",
        subprotocols=None,
        headers=[]
    )
    communicator.scope["url_route"] = {"kwargs": {"product_id": product_id}} 

    connected, _ = await communicator.connect()
    assert connected

    # Simulate an image upload event
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"product_{product_id}",
        {"type": "send_image_update", "image_url": "http://fake-image-url.com/sample.jpg"}
    )

    response = await communicator.receive_json_from()
    assert response == {"event": "image_uploaded", "image_url": "http://fake-image-url.com/sample.jpg"}

    await communicator.disconnect()
