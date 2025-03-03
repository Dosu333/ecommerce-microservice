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
        product_payload["id"] = str(uuid.uuid4())

        response = api_client.post(url, product_payload, format="json")
        assert response.status_code == 201
        assert response.data["status"] == 201

        # Ensure product is inserted into DB
        product = products_collection.find_one({"name": "Laptop"})
        assert product is not None
        products_collection.delete_one({"id": product["id"]})
        
@pytest.mark.django_db
def test_update_product(api_client, product_payload):
    """Test updating a product."""
    # Insert test product into MongoDB
    product_payload["id"] = str(uuid.uuid4())
    inserted_result = products_collection.insert_one(product_payload)
    product = products_collection.find_one({"_id": inserted_result.inserted_id})

    url = f"/api/commerce/products/{product['id']}/"

    # Mock Cloudinary upload
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"secure_url": "http://fake-cloudinary.com/image.jpg"}
        
        updated_data = {
            "name": "Updated Laptop",
            "description": "High performance laptop",
            "price": "999.99",
            "stock": 10,
            "category_id": product["category_id"],
            "images": []
        }

        response = api_client.put(url, updated_data, format="json")

        # Assertions
        assert response.status_code == 200
        assert response.data["status"] == 200

        # Ensure product is updated in MongoDB
        updated_product = products_collection.find_one({"id": product["id"]})
        assert updated_product is not None
        assert updated_product["name"] == "Updated Laptop"

    # Clean up
    products_collection.delete_one({"id": product["id"]})
    

@pytest.mark.django_db
def test_delete_product(api_client, product_payload):
    """Test deleting a product."""
    product_payload["id"] = str(uuid.uuid4())
    inserted_result = products_collection.insert_one(product_payload)
    product = products_collection.find_one({"_id": inserted_result.inserted_id})

    url = f"/api/commerce/products/{product['id']}/"

    response = api_client.delete(url)

    assert response.status_code == 200

    product = products_collection.find_one({"id": product["id"]})
    assert product is None

@pytest.mark.django_db
def test_get_products(api_client, product_payload):
    """Test retrieving products."""
    products_collection.insert_one(product_payload)
    
    url = "/api/commerce/products/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data["data"]) > 0

@pytest.mark.django_db
def test_get_product(api_client, product_payload):
    """Test retrieving a single product."""
    product_payload["id"] = str(uuid.uuid4())
    inserted_result = products_collection.insert_one(product_payload)
    product = products_collection.find_one({"_id": inserted_result.inserted_id})

    url = f"/api/commerce/products/{product['id']}/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["data"]["id"] == product_payload["id"]

    products_collection.delete_one({"id": product["id"]})