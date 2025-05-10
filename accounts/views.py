from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialzers import UserSerializer
from dj_rest_auth.views import LoginView, LogoutView
from .authentication import JWTCookieAuthentication
from django.conf import settings

class Home(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request ):
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

        return response

class CustomLogoutView(LogoutView):
    pass


class GetAccessTokenView(APIView):
    """
    API endpoint to retrieve a valid access token string from the HttpOnly cookie.
    Requires authentication via the HttpOnly cookie.
    """
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests. If the request reaches here, the user is
        authenticated by the HttpOnly cookie. We return the access token.
        """

        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if access_token:
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Authentication successful, but could not retrieve access token from cookies.'},
                status=status.HTTP_400_BAD_REQUEST
            )





