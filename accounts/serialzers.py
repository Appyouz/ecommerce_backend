from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']




# NEW CUSTOM LOGIN SERIALIZER TO ENSURE REFRESH TOKEN IS IN RESPONSE BODY
class CustomJWTLoginSerializer(LoginSerializer):
    """
    Custom Login Serializer to ensure 'access' and 'refresh' tokens
    are always present in the response data for non-cookie authentication.
    """
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        # Get the default representation from the parent class
        ret = super().to_representation(instance)

        # Check if JWT tokens are present and add them to the response data
        # 'instance' here is often the LoginView instance itself,
        # which holds access_token and refresh_token attributes after a successful login.
        if hasattr(self, 'context') and 'request' in self.context:
            request = self.context['request']
            if hasattr(request, 'user') and request.user.is_authenticated:
                # Retrieve tokens from dj_rest_auth's view context or generated tokens
                if hasattr(self.parent, 'access_token') and hasattr(self.parent, 'refresh_token'):
                    ret['access'] = str(self.parent.access_token)
                    ret['refresh'] = str(self.parent.refresh_token)
                # Fallback if direct access via parent is not working (e.g. if the view is not the parent)
                elif hasattr(instance, 'access_token') and hasattr(instance, 'refresh_token'):
                    ret['access'] = str(instance.access_token)
                    ret['refresh'] = str(instance.refresh_token)
                else:
                    # If tokens are still not found, this is a severe misconfiguration.
                    # This branch should ideally not be hit with correct dj_rest_auth setup.
                    print("WARNING: Access and Refresh tokens not found on instance/parent in CustomJWTLoginSerializer.")
                    ret['access'] = "" # Ensure fields are present, even if empty
                    ret['refresh'] = "" # Ensure fields are present, even if empty
            else:
                # Not authenticated, should not have tokens
                ret['access'] = ""
                ret['refresh'] = ""

        # Remove token_type (from Simple JWT payload) if it's there and undesired
        if 'token_type' in ret:
            del ret['token_type']

        return ret
