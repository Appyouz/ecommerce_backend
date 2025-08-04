from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser
from django.core.management import call_command
from django.core.management.base import CommandError

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.filter(seller=self.request.user).order_by('name')

        return Product.objects.all().order_by('name')

    def get_object(self):
        queryset = Product.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    # We now use the serializer's automatic handling of the category and seller,
    # so we only need to provide the seller in the perform_create method.
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    # The serializer's automatic handling also works for updates.
    # No custom perform_update is needed.


class PopulateProductsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        seller_name = request.data.get('seller_name')
        # This line is the key fix: Get json_path from the request payload
        json_path = request.data.get('json_path')

        if not seller_name:
            return Response(
                {'error': 'seller_name is a required field'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the json_path was provided in the request
        if not json_path:
            return Response(
                {'error': 'json_path is a required field'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Pass both seller_name and json_path as named arguments to the command
            call_command('populate_products', seller_name, json_path=json_path)
            return Response(
                {'message': 'Database population command successfully executed.'},
                status=status.HTTP_200_OK
            )
        except CommandError as e:
            return Response(
                {'error': f'An error occured: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occured: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
