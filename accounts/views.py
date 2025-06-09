from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialzers import UserSerializer
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework_simplejwt.tokens import RefreshToken # <--- NEW IMPORT
from django.conf import settings 

class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello world'}
        return Response(content)

# IMPORTANT: Re-introduce CustomLoginView
class CustomLoginView(LoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        # Call the parent's get_response first.
        # This will handle the authentication, but might not add tokens to data.
        response = super().get_response()

        # Try to get the user from the view instance
        user = self.user

        # If user is authenticated, explicitly generate new tokens and add to response
        if user and user.is_authenticated:
            try:
                # Generate new refresh and access tokens directly using Simple JWT
                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)
                refresh_str = str(refresh)

                # Add tokens to the response data
                response.data['access'] = access
                response.data['refresh'] = refresh_str

                # Add user data to the response
                response.data['user'] = UserSerializer(user).data

                # Optional: Remove any 'key' field if it was added by dj-rest-auth for TokenAuth fallback
                if 'key' in response.data:
                    del response.data['key']

                print(f"DEBUG: Tokens successfully injected into response for user {user.username}")
                print(f"DEBUG: Access Token: {access[:20]}...")
                print(f"DEBUG: Refresh Token: {refresh_str[:20]}...")

            except Exception as e:
                print(f"CRITICAL ERROR: Failed to generate/inject tokens or user data: {e}")
                # Might want to return an error response here instead of just printing
                return Response(
                    {'detail': 'Authentication failed due to server token issue.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # If user is not authenticated after super().get_response(),
            # it means login failed, so no tokens should be in response.
            print("DEBUG: CustomLoginView: User not authenticated after super().get_response(). No tokens added.")

        def post(self, request, *args, **kwargs):
            print("DEBUG: Request data:", request.data)
            print("DEBUG: Request content type:", request.content_type)
            return super().post(request, *args, **kwargs)

        return response

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # We don't need to unset cookies here, as frontend clears localStorage.
        return response

