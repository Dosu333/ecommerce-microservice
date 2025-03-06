import uuid
from django.utils.text import slugify
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config
from core.database import products_collection, categories_collection
from core.permissions import IsCustomer, IsVendor
from core.pagination import CustomPagination
from core.utils import upload_images
from .serializers import CategorySerializer, CreateProductSerializer, ListProductSerializer, UpdateProductSerializer
from .tasks import upload_product_image_to_cloudinary, update_category_name


class CategoryAPIView(views.APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated] 
        if self.request.method != 'GET':
            permission_classes.append(IsVendor) 
        return [permission() for permission in permission_classes]

    def get(self, request, category_id=None):
        if category_id:
            category = categories_collection.find_one({"id": category_id}, {"_id": 0})
            if not category:
                return Response({'status': 404, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(category)
            return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)
        paginator = CustomPagination()
        query_filter = {"vendor_id": request.user.id} if IsVendor().has_permission(request, self) else {}
        categories_cursor = categories_collection.find(query_filter, {"_id": 0})
        paginated_categories = paginator.paginate_queryset(categories_cursor, request)
        
        if not paginated_categories:
            return Response({"message": "No categories found"}, status=200)

        # Serialize and return response
        data = self.serializer_class(paginated_categories, many=True).data
        return paginator.get_paginated_response(data)
    
    def post(self, request):
        data = request.data.copy()
        data['vendor_id'] = request.user.id
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category_data = serializer.validated_data
            category_data['id'] = str(uuid.uuid4())
            category_data['slug'] = slugify(category_data['name']) + '-' + category_data['id'][:8]
            categories_collection.insert_one(category_data)
            return Response({'status': 200, 'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id):
        category = categories_collection.find_one({"id": category_id})
        if not category:
            return Response({'status': 404, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_data = serializer.validated_data
            categories_collection.update_one({"id": category_id}, {"$set": category_data})
            update_category_name.apply_async((category_id, category_data['name']))
            return Response({'status': 200, 'message': 'Category updated successfully'}, status=status.HTTP_200_OK)
        
        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id):
        category = categories_collection.find_one({"id": category_id})
        if not category:
            return Response({'status': 404, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        categories_collection.delete_one({"id": category_id})
        return Response({'status': 200, 'message': 'Category deleted successfully'}, status=status.HTTP_200_OK)
    

class ProductAPIView(views.APIView):
    serializer_class = ListProductSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_classes.append(IsVendor)
        return [permission() for permission in permission_classes]

    def get(self, request, product_id=None):
        """Handles GET requests with search capabilities."""
        if product_id:
            product = products_collection.find_one({"id": product_id}, {"_id": 0})
            if not product:
                return Response({'status': 404, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(product)
            return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)

        # Get query params
        search_query = request.query_params.get('q', None)
        category_name = request.query_params.get('category', None)
        vendor_id = request.query_params.get('vendor', None)

        # Define the query
        query = {}

        # Search by name and description
        if search_query:
            query["name"] = {"$regex": search_query, "$options": "i"}
            query['description'] = {"$regex": search_query, "$options": "i"}

        # Filter by category
        if category_name:
            query["category_name"] = {"$regex": category_name, "$options": "i"}

        # Filter by vendor
        if vendor_id:
            query["vendor_id"] = vendor_id

        # Get products based on filters
        products_cursor = products_collection.find(query, {"_id": 0})

        # Implement pagination
        paginator = CustomPagination()
        paginated_products = paginator.paginate_queryset(products_cursor, request)

        # Serialize and return results
        data = self.serializer_class(paginated_products, many=True).data
        return paginator.get_paginated_response(data)

    def post(self, request):
        data = request.data.copy()
        data['vendor_id'] = request.user.id
        serializer = CreateProductSerializer(data=data)
        websocket_url = config('WEBSOCKET_URL')
        
        if serializer.is_valid():
            product_data = serializer.validated_data
            product_data['id'] = str(uuid.uuid4())
            images = request.FILES.getlist('images', [])
            product_data['images'] = []
            product_data['price'] = float(product_data['price'])
            product_data['slug'] = slugify(product_data['name']) + '-' + product_data['id'][:8]
            products_collection.insert_one(product_data)
            
            for image in images:
                upload_product_image_to_cloudinary.apply_async((image.read(), product_data['id']))
            
            return Response({
                'status': 201, 
                'message': 'Product created successfully',
                'images_uploaded': len(images),
                'websocket_url': f'{websocket_url}/products/{product_data["id"]}/' if images else None
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
                'images_uploaded': len(images),
                'websocket_url': f'{websocket_url}/products/{product_id}/' if images else None
            }, status=status.HTTP_200_OK)

        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = products_collection.find_one({"id": product_id})
        if not product:
            return Response({'status': 404, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        products_collection.delete_one({"id": product_id})
        return Response({'status': 200, 'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)