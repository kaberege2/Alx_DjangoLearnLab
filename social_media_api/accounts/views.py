from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated

# User registration view
class RegisterView(views.APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # Create the user and the token
            token = Token.objects.get(user=user)  # Get the token associated with the user
            return Response({"token": token.key,'message': 'User registered successfully!','username': user.username,
                'bio': user.bio,
                'profile_picture': user.profile_picture.url if user.profile_picture else None}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login view
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Authenticate the user
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                # Get or create a token for the user
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User profile view (for authenticated users)
class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the current user's profile details
        user = request.user
        data = {
            'username': user.username,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
        }
        return Response(data)

