from dj_rest_auth.views import APIView

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response 
from rest_framework import status,  viewsets
from cart.serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem
from django.db import transaction 


# helper function to get or create the user's cart
def get_or_create_cart(user):
    """Gets the cart for the given user, creating one if it doesn't exist."""
    cart, created = Cart.objects.get_or_create(user=user)

    # Log
    print(f"Cart for user {user.username} {'created' if created else 'fetched'}.")

    return cart

class UserCartView(APIView):
    """
    API endpoint to view the authenticated user's shopping cart.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request ):
        """Handles GET requests to view the user's cart."""
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartItemAddView(APIView):
    """
    API endpoint to add a product to the authenticated user's cart.
    Requires authentication.
    Accepts POST requests with 'product_id' and 'quantity'.
    If the product is already in the cart, updates the quantity.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request ):
        """Handles POST requests to add a product to the cart."""

        cart = get_or_create_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Access the validated data
        product_id = serializer.validated_data['product'].id
        quantity = serializer.validated_data.get('quantity', 1)

        if quantity < 1:
            return Response({"quantity": "Quantity must be at least 1."}, status=status.HTTP_400_BAD_REQUEST)

        # logic to add/ update item
        with transaction.atomic():
            try:
                # check if item already exists
                cart_item = CartItem.objects.get(cart=cart, product__id=product_id)

                # if item exists update its quantity
                cart_item.quantity += quantity
                cart_item.save()

                response_serializer = CartItemSerializer(cart_item)

                return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
            
            except CartItem.DoesNotExist:
                # if doenst exist create a new cartItem
                serializer.save(cart=cart)

                response_serializer = CartItemSerializer(serializer.instance)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authenticated users to retrieve, update, or delete
    individual items in their own cart.
    Requires authentication.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_or_create_cart(self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_update(self, serializer):
        quantity = serializer.validated_data.get('quantity', serializer.instance.quantity)

        if quantity < 1:
           return Response({"quantity": "Quantity must be at least 1."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()


