from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CartItemAddView, UserCartView, CartItemViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', UserCartView.as_view(), name='user-cart'),
    path('items/', CartItemAddView.as_view(), name='cart-item-add'),
    path('', include(router.urls)),
]
