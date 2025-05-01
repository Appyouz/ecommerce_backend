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

    def get(self, request ):
        content = {'message': 'Hello world'}
        return Response(content)

class CustomLoginView(LoginView):
    permission_classes = [AllowAny]
    
    @override
    def get_response(self):

        print("--- DEBUG: Entering CustomLoginView get_response ---")
        response = super().get_response()

        print("--- DEBUG: Response headers AFTER super():", dict(response.headers))
        user = self.user
        if response and hasattr(response, 'data') and isinstance(response.data, dict) and user and user.is_authenticated:
            print("--- DEBUG: Checks passed, attempting to add user data ---")
            try:
                response.data['user'] = UserSerializer(user).data
                print("--- DEBUG: Successfully added user data ---")

                print("--- DEBUG: Response headers AFTER data modification:", dict(response.headers))
            except Exception as e:
                 print(f"--- DEBUG: Error adding user data to login response: {e} ---")
                 print("--- DEBUG: Response headers IN CATCH block:", dict(response.headers)) # Check headers even in error
                # print(f"Error adding user data to login response: {e}")

        print("--- DEBUG: Exiting CustomLoginView get_response ---")
        return response

class CustomLogoutView(LogoutView):
    pass
