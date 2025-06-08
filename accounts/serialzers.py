from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CustomJWTLoginSerializer(LoginSerializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # This serializer is used by the CustomLoginView's get_response.
        # We need to ensure the tokens are passed through, or generated if not already.
        # Note: In CustomLoginView, we are explicitly generating and adding them,
        # so this serializer's to_representation might just be confirming/passing them.
        # The CustomLoginView's get_response will take precedence for token injection.
        # This serializer mostly ensures the expected fields are defined.

        return ret
