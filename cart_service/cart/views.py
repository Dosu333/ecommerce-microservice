from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCustomer
from .serializers import CartItemSerializer
from .services import CartService

class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the cart from Redis."""
        cart = CartService.get_cart(request.user.id)
        return Response({"status": 200, "data":cart}, status=status.HTTP_200_OK)

    def post(self, request):
        """Add an item to the cart."""
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            cart = CartService.add_to_cart(request.user.id, str(data["product_id"]), data["quantity"])
            return Response({"status": 201, "message": "Item added to cart", "data": cart}, status=status.HTTP_201_CREATED)
        return Response({"status": 400, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Remove an item from the cart."""
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"status": 400, "errors": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = CartService.remove_from_cart(request.user.id, product_id)
        return Response({"status": 200, "message": "Item removed from cart", "data":cart}, status=status.HTTP_200_OK)

class PersistCartView(views.APIView):
    """Move cart from Redis to PostgreSQL when the user checks out."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = CartService.persist_cart(request.user.id)
        if cart:
            return Response({"status": 201, "message": "Cart saved successfully", "cart_id": cart.id}, status=status.HTTP_201_CREATED)
        return Response({"status": 200, "message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
