from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialzers import UserSerializer
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.jwt_auth import set_jwt_cookies, unset_jwt_cookies
from .authentication import JWTCookieAuthentication
from django.conf import settings

class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello world'}
        return Response(content)

class CustomLoginView(LoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        response = super().get_response()

        user = self.user
        if response and hasattr(response, 'data') and isinstance(response.data, dict) and user and user.is_authenticated:
            try:
                response.data['user'] = UserSerializer(user).data
            except Exception as e:
                print(f"Error adding user data to login response: {e}")

            # Set the JWT cookies
            set_jwt_cookies(response, self.access_token, self.refresh_token)

        return response

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Unset the JWT cookies
        unset_jwt_cookies(response)

        return response

class GetAccessTokenView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if access_token:
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Authentication successful, but could not retrieve access token from cookies.'},
                status=status.HTTP_400_BAD_REQUEST
            )
