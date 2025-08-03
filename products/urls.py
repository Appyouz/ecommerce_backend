
from django.urls import path, include
from rest_framework.routers import DefaultRouter # Import DefaultRouter

from .views import ProductViewSet, CategoryViewSet, PopulateProductsView

# Create a router and register our viewsets with it.
# DefaultRouter automatically sets up URLs for list, create, retrieve, update, partial_update, and destroy actions.
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products') # Register ProductViewSet at '/products/'
router.register(r'categories', CategoryViewSet) # Register CategoryViewSet at '/categories/'

urlpatterns = [
    path('populate_db/', PopulateProductsView.as_view(), name='populate_db'),
    path('', include(router.urls)),
]

