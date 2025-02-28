from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()

class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    # image = serializers.ImageField()