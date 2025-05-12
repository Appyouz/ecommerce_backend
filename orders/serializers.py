from rest_framework import serializers

from products.serializers import ProductSerializer
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    Includes nested Product details for read operations.
    """

    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'quantity', 'get_total_item_price', 'created_at', 'updated_at']
        read_only_fields = ['order', 'product', 'product_name', 'product_price', 'get_total_item_price', 'created_at', 'updated_at']





class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    Includes nested OrderItem serializers to show items in the order.
    """

    items = OrderItemSerializer(many=True, read_only=True)

    # To show the username instead of user id
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Order

        fields = ['id', 'user', 'items', 'total_amount', 'status', 'created_at', 'updated_at' ]
        read_only_fields = ['user', 'items', 'total_amount', 'created_at', 'updated_at']

