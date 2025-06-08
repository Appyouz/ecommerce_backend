from django.urls import path

from .views import Home 

urlpatterns = [
    path('', Home.as_view()),
    # path('login/', CustomLoginView.as_view(), name='rest_login'),
    # path('logout/', CustomLogoutView.as_view(), name='rest_logout'),

    # path('auth/get-token/', GetAccessTokenView.as_view(), name='get-access-token'),
]
