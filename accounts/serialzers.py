from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, SellerProfile

User = get_user_model()

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['store_name', 'business_email', 'phone_number', 'business_address', 'tax_id']


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display')
    seller_profile = SellerProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'seller_profile']


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

class SellerRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    seller_profile = SellerProfileSerializer()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username already exists."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email already exists."})
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        seller_profile_data = validated_data.pop('seller_profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
            role='SELLER'
        )

        SellerProfile.objects.create(user=user, **seller_profile_data)
        return user
                 
