from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

        # Ready only cannot be updated and shouldn't be
        read_only_fields = ['created_at', 'updated_at']



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')
