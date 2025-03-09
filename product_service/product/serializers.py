from rest_framework import serializers
from core.exceptions import CustomValidationError
from core.database import categories_collection, reviews_collection, products_collection
from core.utils import get_user
import uuid


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(required=False)


class VendorSerializer(UserSerializer):
    company = serializers.CharField(required=False)
    
    
class ReviewSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    product_id = serializers.CharField(max_length=225)
    user_id = serializers.CharField(max_length=225, read_only=True)
    user = serializers.SerializerMethodField("get_user_details")
    rating = serializers.IntegerField()
    review = serializers.CharField()
    
    def validate_rating(self, value):
        if value > 5 or value < 0:
            raise CustomValidationError("You can only give a rate between 0 and 5")
        return value
    
    def validate_product_id(self, value):
        product = products_collection.find_one({"id": value})
        if not product:
            raise CustomValidationError("Product does not exist")
        return value
    
    def get_user_details(sel, obj):
        user = get_user(obj["user_id"])
        return UserSerializer(user).data
    

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    vendor_id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False)
    attributes = serializers.ListField(child=serializers.CharField(), required=False, default=[])
    is_active = serializers.BooleanField(default=False)
    
    def validate_name(self, value):
        category = categories_collection.find_one({"name": value, "vendor_id": self.initial_data.get("vendor_id")})
        if category:
            raise CustomValidationError("Category with this name already exists")
        return value
    
class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    vendor_id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_rating = serializers.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    stock = serializers.IntegerField() 
    attributes = serializers.DictField(child=serializers.CharField(), required=False, default={})
    is_active = serializers.BooleanField(default=False)


class CreateProductSerializer(ProductSerializer):
    category_id = serializers.CharField(max_length=255, write_only=True)
    category_name = serializers.CharField(max_length=255)
    
    def validate_attributes(self, value):
        category = categories_collection.find_one({"id": self.initial_data["category_id"], "vendor_id": self.initial_data["vendor_id"]})
        for attribute in value:
            if attribute not in category["attributes"]:
                raise CustomValidationError(f"Invalid attribute: {attribute} for category: {category['name']}")
        return value   
    
    def validate_category_id(self, value):
        category = categories_collection.find_one({"id": value})
        if not category:
            raise CustomValidationError("Invalid category_id")
        if category["vendor_id"] != self.initial_data["vendor_id"]:
            raise CustomValidationError("You can only create products for your own categories")
        self.initial_data["category_name"] = category["name"]
        return value


class ListProductSerializer(ProductSerializer):
    images = serializers.ListField(child=serializers.URLField(), read_only=True, default=[])
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        category = categories_collection.find_one({"id": obj["category_id"]})
        return CategorySerializer(category).data
    
class RetrieveProductSerializer(ListProductSerializer):
    vendor = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    
    def get_vendor(self, obj):
        vendor = get_user(obj["vendor_id"])
        return VendorSerializer(vendor).data
    
    def get_reviews(self, obj):
        reviews = reviews_collection.find({"product_id": obj["id"]})
        return ReviewSerializer(reviews, many=True).data
    

class UpdateProductSerializer(CreateProductSerializer):
    remove_images = serializers.ListField(child=serializers.URLField(), required=False, default=[])