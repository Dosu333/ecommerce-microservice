from rest_framework import serializers
from core.exceptions import CustomValidationError
from core.database import categories_collection


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    category_id = serializers.CharField(max_length=255, write_only=True)
    category = serializers.SerializerMethodField()
    
    def validate_category_id(self, value):
        category = categories_collection.find_one({"id": value})
        if not category:
            raise CustomValidationError("Invalid category_id")
        return value
    
    def get_category(self, obj):
        category = categories_collection.find_one({"id": obj["category_id"]})
        return CategorySerializer(category).data