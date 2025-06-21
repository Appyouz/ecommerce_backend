from django.urls import path

from .views import Home, SellerDashboardView, SellerRegistrationView

urlpatterns = [
    path('', Home.as_view()),
    path('register/seller/', SellerRegistrationView.as_view(), name='seller_register'),
    path('seller/dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
]
