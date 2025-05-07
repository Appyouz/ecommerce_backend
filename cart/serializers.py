from rest_framework import serializers
from products.serializers import ProductSerializer
from products.models import Product
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'product_id', 'created_at', 'updated_at']
        read_only_fields = ('cart', 'created_at', 'updated_at')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj: Cart): 
        total = sum(item.product.price * item.quantity for item in obj.items.all() if item.product) # type: ignore
        return round(total, 2)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ('user', 'created_at', 'updated_at')
