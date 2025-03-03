import pytest
from unittest.mock import patch
from product.tasks import upload_product_image_to_cloudinary
from core.database import products_collection, categories_collection
import uuid


@pytest.mark.django_db
def test_upload_product_image_to_cloudinary():
    """Test Celery task for uploading images to Cloudinary."""
    product_id = str(uuid.uuid4())
    catgory_id = str(uuid.uuid4())
    category_data = {"id": catgory_id, "name": "Electronics"}
    category = categories_collection.insert_one(category_data)
    product_data = {
        "id": product_id,
        "name": "Laptop",
        "description": "High performance laptop",
        "price": 999.99,
        "stock": 10,
        "category_id": catgory_id,
        "images": []
    }
    products_collection.insert_one(product_data)
    
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"secure_url": "http://fake-cloudinary.com/image.jpg"}

        image_data = b"fake_image_data"
        result = upload_product_image_to_cloudinary(image_data, product_id)

        assert result == "http://fake-cloudinary.com/image.jpg"
        
        product = products_collection.find_one({"id": product_id})
        print(product)
        assert "http://fake-cloudinary.com/image.jpg" in product["images"]
