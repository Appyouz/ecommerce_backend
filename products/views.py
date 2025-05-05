from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

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
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
        serializer.save(category=category)



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


