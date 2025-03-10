from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import CartService

class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the cart from Redis."""
        cart = CartService.get_cart(request.user.id)
        return Response(cart, status=status.HTTP_200_OK)

    def post(self, request):
        """Add an item to the cart."""
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = CartService.add_to_cart(request.user.id, product_id, quantity)
        return Response(cart, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """Remove an item from the cart."""
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = CartService.remove_from_cart(request.user.id, product_id)
        return Response(cart, status=status.HTTP_200_OK)

class PersistCartView(views.APIView):
    """Move cart from Redis to PostgreSQL when the user checks out."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = CartService.persist_cart(request.user.id)
        if cart:
            return Response({"message": "Cart saved successfully", "cart_id": cart.id}, status=status.HTTP_201_CREATED)
        return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
