from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from django.db import transaction 
from django.core.exceptions import ObjectDoesNotExist 

from .serializers import OrderSerializer # Only need OrderSerializer for the response
from .models import Order, OrderItem # Need Order and OrderItem models

from cart.models import Cart # Need Cart model to fetch the user's cart



class OrderCreateView(APIView):
    """
    API endpoint to create an order from the authenticated user's cart.
    Requires authentication.
    Accepts POST requests.
    """
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        """
        Handles POST requests to create an order from the user's cart.
        """
        # 1. Get the authenticated user's cart
        # Use Cart.objects.get to ensure the cart exists for the current user.
        # If it doesn't exist, ObjectDoesNotExist exception is raised.
        try:
            cart = Cart.objects.get(user=request.user)
            print(f"Fetched cart for user {request.user.username}.")
        except ObjectDoesNotExist:
            # If the user somehow doesn't have a cart, or it was deleted unexpectedly
            print(f"User {request.user.username} does not have a cart.") 
            return Response({"detail": "User does not have a cart."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Check if the cart has items
        # Use select_related('product') to fetch related product data in one query
        cart_items = cart.items.select_related('product').all() # Get all items related to this cart
        if not cart_items:
            # If the cart is empty, cannot create an order
            print("Cart is empty. Cannot create order.") 
            return Response({"detail": "Your cart is empty. Add items before creating an order."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Start a Database Transaction
        # This ensures atomicity: either the whole order creation succeeds, or none of it does.
        with transaction.atomic():
            order = Order(user=request.user, status='Pending')
            print(f"Instantiated Order for user {request.user.username}.") 


            # Initialize total amount calculation
            calculated_total_amount = 0

            # 5. Process Cart Items and Create Order Items
            order_items_to_create = [] # List to hold OrderItem instances before bulk creation (optional, but can be faster)
            for cart_item in cart_items:
                 # Might want to add a stock check here before creating the order item
                 # e.g., if cart_item.quantity > cart_item.product.stock: return error
                 # If stock check fails, would rollback the transaction and return an error.

                # Create an OrderItem for each CartItem
                order_item = OrderItem(
                    order=order, # Link the order item to the newly created order instance (it doesn't need an ID yet)
                    product=cart_item.product, # Link to the original product (optional but good practice)
                    product_name=cart_item.product.name, # Copy the name
                    product_price=cart_item.product.price, # Copy the price AT THE TIME OF ORDER
                    quantity=cart_item.quantity # Copy the quantity from the cart item
                )
                order_items_to_create.append(order_item)

                # Add this item's price * quantity to the calculated total
                # Using the stored product_price from the OrderItem instance we just created
                calculated_total_amount += order_item.get_total_item_price # Use the @property for calculation

                print(f"Prepared OrderItem for product: {order_item.product_name} (Quantity: {order_item.quantity}, Price: {order_item.product_price}).")

            # 6. Calculate and Save the Order Total
            # Update the order instance with the final calculated total amount
            order.total_amount = calculated_total_amount
            order.save() # Now save the Order instance. This will assign it a primary key.
            print(f"Order {order.id} saved with total amount: {order.total_amount}")

            # Bulk create OrderItems for efficiency
            # This saves all the OrderItem instances linked to the new order instance (which now has an ID)
            OrderItem.objects.bulk_create(order_items_to_create)
            print(f"Bulk created {len(order_items_to_create)} OrderItems for Order {order.id}.") 

            # 7. Clear the Cart
            # Delete all cart items belonging to this cart to empty it
            # This will trigger the deletion of CartItem instances
            cart_items.delete()
            print(f"Cart items for cart {cart.id} deleted.")
            # Note: The Cart instance itself is NOT deleted, just its items.
            # The cart instance remains linked to the user, ready for new items.


            # 8. Return Response
            # Serialize the newly created order for the response
            # Use the OrderSerializer with nested items
            serializer = OrderSerializer(order)

            # Return the serialized order data with a 201 Created status
            print(f"Order {order.id} creation successful. Returning response.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

