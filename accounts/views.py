from typing import override
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serialzers import UserSerializer
from dj_rest_auth.views import LoginView, LogoutView


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self ):
        content = {'message': 'Hello world'}
        return Response(content)

class CustomLoginView(LoginView):
    permission_classes = [AllowAny]
    
    @override
    def get_response(self):
        response = super().get_response()
        user = self.user
        if response and hasattr(response, 'data') and isinstance(response.data, dict) and user and user.is_authenticated:
            try:
                response.data['user'] = UserSerializer(user).data
            except Exception as e:
                print(f"Error adding user data to login response: {e}")

        return response

class CustomLogoutView(LogoutView):
    pass
