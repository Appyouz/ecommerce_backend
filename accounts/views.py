from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialzers import UserSerializer
from dj_rest_auth.views import LoginView, LogoutView

class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello world'}
        return Response(content)

class CustomLoginView(LoginView):
    permission_classes = [AllowAny]

    def get_response(self):
        # Call the parent's get_response first.
        response = super().get_response()

        user = self.user
        if response and hasattr(response, 'data') and isinstance(response.data, dict) and user and user.is_authenticated:
            try:
                # Add user data to the response. This is good practice.
                response.data['user'] = UserSerializer(user).data
            except Exception as e:
                print(f"Error adding user data to login response: {e}")

            # CRITICAL FIX: Explicitly add 'access' and 'refresh' tokens to the response data.
            # Frontend expects these keys in the response body.
            # We are taking them from the `self.access_token` and `self.refresh_token` attributes
            # that `dj-rest-auth`'s LoginView has prepared.
            if hasattr(self, 'access_token') and self.access_token:
                response.data['access'] = str(self.access_token)
            else:
                # This should ideally not happen if JWT is used and login is successful
                print("WARNING: access_token not found on self after super().get_response() in CustomLoginView.")

            if hasattr(self, 'refresh_token') and self.refresh_token:
                response.data['refresh'] = str(self.refresh_token)
            else:
                # This is the problem I've been facing! It means refresh_token wasn't
                # being added to the response data, even if it was generated internally.
                print("WARNING: refresh_token not found on self after super().get_response() in CustomLoginView.")
                # Ensure it's explicitly set to an empty string if not present, to match frontend expectation
                response.data['refresh'] = ""


        return response

class CustomLogoutView(LogoutView):
    # This class should now correctly clear tokens (if any) and sessions via dj-rest-auth's default.
    # No custom code needed here. The default LogoutView handles JWT blacklisting and session clearing.
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
