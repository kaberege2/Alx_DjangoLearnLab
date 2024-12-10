from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Custom user model
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    # We do not expose the password in the serializer
    password = serializers.CharField(write_only=True)

    # Ensure the profile_picture is a file field
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Automatically hash the password and create the user
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Create an authentication token for the user
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
