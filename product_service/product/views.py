import uuid
from rest_framework import views, status
from rest_framework.response import Response
from decouple import config
from core.database import products_collection, categories_collection
from core.utils import upload_images
from .serializers import ProductSerializer, CategorySerializer
from .tasks import upload_product_image_to_cloudinary


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
    serializer_class = ProductSerializer
    
    def get(self, request):
        products = products_collection.find({}, {"_id": 0})
        serializer = ProductSerializer(products, many=True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        placeholder_image = config('PRODUCT_PLACEHOLDER_IMAGE_URL')
        websocket_url = config('WEBSOCKET_URL')
        
        if serializer.is_valid():
            product_data = serializer.validated_data
            product_data['id'] = str(uuid.uuid4())
            images = request.FILES.getlist('images', [])
            product_data['images'] = [placeholder_image] * len(images) if len(images) else [placeholder_image]
            product_data['price'] = float(product_data['price'])
            products_collection.insert_one(product_data)
            
            for image in images:
                upload_product_image_to_cloudinary.apply_async(image.read(), product_data['id'])
            
            return Response({
                'status': 200, 
                'message': 'Product created successfully',
                'websocket_url': f'{websocket_url}/products/{product_data["id"]}/'
                }, status=status.HTTP_201_CREATED)
        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)