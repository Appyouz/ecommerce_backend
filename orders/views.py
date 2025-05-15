from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from django.db import transaction 
from django.core.exceptions import ObjectDoesNotExist 

from .serializers import OrderSerializer # Only need OrderSerializer for the response
from .models import Order, OrderItem # Need Order and OrderItem models

from cart.models import Cart # Need Cart model to fetch the user's cart

from rest_framework import generics


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list authenticated user's orders and create a new order
     from the user's cart.
    Requires authentication.
    Handles GET (list) and POST (create).
    """
    serializer_class = OrderSerializer # Use OrderSerializer for both listing and creating response
    permission_classes = [IsAuthenticated] # Only authenticated users

    # Method for handling GET requests (Listing Orders)
    def get_queryset(self):
        """
        Returns the list of orders for the currently authenticated user.
        """
        # Filter orders to only include those belonging to the current user
        return Order.objects.filter(user=self.request.user).order_by('-created_at') # Order by newest first

    # Method for handling POST requests (Creating Order from Cart)
    # This logic is adapted from the previous OrderCreateView's post method
    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create an order from the user's cart.
        This overrides the default create method of ListCreateAPIView.
        """
        # 1. Get the authenticated user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            print(f"Fetched cart for user {request.user.username}.")
        except ObjectDoesNotExist:
            print(f"User {request.user.username} does not have a cart.")
            return Response({"detail": "User does not have a cart."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Check if the cart has items
        cart_items = cart.items.select_related('product').all()
        if not cart_items:
            print("Cart is empty. Cannot create order.")
            return Response({"detail": "Your cart is empty. Add items before creating an order."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Start a Database Transaction
        with transaction.atomic():
            # 4. Create the Order (Instantiate without saving immediately)
            order = Order(user=request.user, status='Pending')
            print(f"Instantiated Order for user {request.user.username}.")

            # Initialize total amount calculation
            calculated_total_amount = 0

            # 5. Process Cart Items and Create Order Items
            order_items_to_create = []
            for cart_item in cart_items:
                 # Optional: Add stock check here if needed
                order_item = OrderItem(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
                order_items_to_create.append(order_item)
                calculated_total_amount += order_item.get_total_item_price

                print(f"Prepared OrderItem for product: {order_item.product_name} (Quantity: {order_item.quantity}, Price: {order_item.product_price}).")


            # 6. Calculate and Save the Order Total
            order.total_amount = calculated_total_amount
            order.save() # Save the Order instance to get its primary key

            # Bulk create OrderItems
            OrderItem.objects.bulk_create(order_items_to_create)
            print(f"Bulk created {len(order_items_to_create)} OrderItems for Order {order.id}.")

            # 7. Clear the Cart
            cart_items.delete()
            print(f"Cart items for cart {cart.id} deleted.")

            # 8. Return Response
            # Use the serializer_class defined on the ListCreateAPIView
            serializer = self.get_serializer(order) # Use self.get_serializer()

            # Return the serialized order data with a 201 Created status
            print(f"Order {order.id} creation successful. Returning response.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

