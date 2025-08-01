from itertools import product
from typing import override
from django_filters import filterset
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Viewset for the cateogry model
# Provides CRUD operations for categories
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name') # define base queryset
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    @override
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('name')

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    # filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

    @override
    def get_object(self):
        queryset = Product.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj



    # Method called when creating a new object
    def perform_create(self, serializer):
        category_id = self.request.data.get('category_id')
        category = None
        if category_id:
            try: 
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                # Handle raise where category id isn't valid
                pass

        # If found save the serializer by passing the instance of category
        serializer.save(category=category,seller=self.request.user)



    def perform_update(self, serializer):
         # Check if 'category_id' was provided in the request data
        category_id = self.request.data.get('category_id')
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                 pass
        elif category_id is None and 'category_id' in self.request.data:
             # Handle case where category_id is explicitly sent as null to unset the category
             category = None


        # Save the serializer, passing the category instance if found
        # The serializer's update method will receive 'category' in validated_data
        # If category_id was not in data, the existing instance's category will be used by default
        serializer.save(category=category)


