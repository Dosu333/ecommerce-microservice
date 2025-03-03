import json
import uuid
import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from core.database import products_collection, categories_collection
from decouple import config

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def category():
    category_data = {"id": str(uuid.uuid4()), "name": "Electronics"}
    categories_collection.insert_one(category_data)
    yield category_data
    categories_collection.delete_one({"id": category_data["id"]})

@pytest.fixture
def product_payload(category):
    return {
        "name": "Laptop",
        "description": "High performance laptop",
        "price": "999.99",
        "stock": 10,
        "category_id": category["id"],
        "images": []
    }

@pytest.mark.django_db
def test_create_product(api_client, product_payload):
    """Test creating a product."""
    url = "/api/commerce/products/"
    
    # Mock Cloudinary upload
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"secure_url": "http://fake-cloudinary.com/image.jpg"}

        response = api_client.post(url, product_payload, format="json")
        assert response.status_code == 201
        assert response.data["status"] == 200
        assert "Product created successfully" in response.data["message"]

        # Ensure product is inserted into DB
        product = products_collection.find_one({"name": "Laptop"})
        assert product is not None
        # products_collection.delete_one({"id": product["id"]})

@pytest.mark.django_db
def test_get_products(api_client, product_payload):
    """Test retrieving products."""
    products_collection.insert_one(product_payload)
    
    url = "/api/commerce/products/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data["data"]) > 0
