from rest_framework import serializers
from core.exceptions import CustomValidationError
from core.database import categories_collection


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField(required=False)
    attributes = serializers.ListField(child=serializers.CharField(), required=False, default=[])
    
    def validate_name(self, value):
        category = categories_collection.find_one({"name": value})
        if category:
            raise CustomValidationError("Category with this name already exists")
        return value
    

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    attributes = serializers.DictField(child=serializers.CharField(), required=False, default={})
    
    def validate_attributes(self, value):
        category = categories_collection.find_one({"id": self.initial_data["category_id"]})
        for attribute in value:
            if attribute not in category["attributes"]:
                raise CustomValidationError(f"Invalid attribute: {attribute} for category: {category['name']}")
        return value    
    

class CreateProductSerializer(ProductSerializer):
    category_id = serializers.CharField(max_length=255, write_only=True)
    
    def validate_category_id(self, value):
        category = categories_collection.find_one({"id": value})
        if not category:
            raise CustomValidationError("Invalid category_id")
        return value


class ListProductSerializer(ProductSerializer):
    images = serializers.ListField(child=serializers.URLField(), read_only=True, default=[])
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        category = categories_collection.find_one({"id": obj["category_id"]})
        return CategorySerializer(category).data
    

class UpdateProductSerializer(CreateProductSerializer):
    remove_images = serializers.ListField(child=serializers.URLField(), required=False, default=[])