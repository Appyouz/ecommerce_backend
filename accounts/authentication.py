from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.conf import settings

class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to get the token from the cookie
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        if access_token:
            # If token is in cookie, validate it
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        
        # If no token in cookie, let parent class check Authorization header
        return super().authenticate(request)
