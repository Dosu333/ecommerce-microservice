from rest_framework import views, status
from rest_framework.response import Response
from core.database import products_collection, categories_collection
from .serializers import CreateProductSerializer, CategorySerializer
from decimal import Decimal
import uuid


class CategoryAPIView(views.APIView):
    serializer_class = CategorySerializer
    
    def get(self, request):
        categories = categories_collection.find({}, {"_id": 0})
        return Response({'status': 200, 'data': list(categories)}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_data = serializer.validated_data
            category_data['id'] = str(uuid.uuid4())
            categories_collection.insert_one(category_data)
            return Response({'status': 200, 'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductAPIView(views.APIView):
    serializer_class = CreateProductSerializer
    
    def get(self, request):
        products = products_collection.find({}, {"_id": 0})
        return Response({'status': 200, 'data': list(products)}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            product_data = serializer.validated_data
            product_data['id'] = str(uuid.uuid4())
            
            for key, value in product_data.items():
                if isinstance(value, Decimal):
                    product_data[key] = float(value)
            
            products_collection.insert_one(product_data)
            return Response({'status': 200, 'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)