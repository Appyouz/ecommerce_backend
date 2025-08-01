from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

        # Ready only cannot be updated and shouldn't be
        read_only_fields = ['created_at', 'updated_at']



class ProductSerializer(serializers.ModelSerializer):
    category  = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )    
    # Add seller to the list of fields. It will be automatically set by the view but should
    # be shown in the response.
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image', 'seller', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at', 'seller')

    # price validation
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value
