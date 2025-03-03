import uuid
from rest_framework import views, status
from rest_framework.response import Response
from decouple import config
from core.database import products_collection, categories_collection
from core.utils import upload_images
from .serializers import CategorySerializer, CreateProductSerializer, ListProductSerializer, UpdateProductSerializer
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
    serializer_class = ListProductSerializer
    
    def get(self, request):
        products = products_collection.find({}, {"_id": 0})
        serializer = ListProductSerializer(products, many=True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
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
                'status': 201, 
                'message': 'Product created successfully',
                'websocket_url': f'{websocket_url}/products/{product_data["id"]}/'
                }, status=status.HTTP_201_CREATED)
        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, product_id):
        product = products_collection.find_one({"id": product_id})
        if not product:
            return Response({'status': 404, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateProductSerializer(data=request.data)
        if serializer.is_valid():
            product_data = serializer.validated_data
            images = request.FILES.getlist('images', [])
            remove_images = request.data.get('remove_images', [])
            placeholder_image = config('PRODUCT_PLACEHOLDER_IMAGE_URL')
            websocket_url = config('WEBSOCKET_URL')

            existing_images = product.get("images", [])

            # Remove images specified in `remove_images`
            updated_images = [img for img in existing_images if img not in remove_images]
            new_placeholder_images = [placeholder_image] * len(images)
            product_data['images'] = updated_images + new_placeholder_images if images else updated_images

            if "price" in product_data:
                product_data['price'] = float(product_data['price'])

            # Update product in DB
            update_fields = {"$set": product_data}
            products_collection.update_one({"id": product_id}, update_fields)

            # Upload new images to Cloudinary asynchronously
            for image in images:
                upload_product_image_to_cloudinary.apply_async((image.read(), product_id))

            return Response({
                'status': 200,
                'message': 'Product updated successfully',
                'websocket_url': f'{websocket_url}/products/{product_id}/'
            }, status=status.HTTP_200_OK)

        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = products_collection.find_one({"id": product_id})
        if not product:
            return Response({'status': 404, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        products_collection.delete_one({"id": product_id})
        return Response({'status': 200, 'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)