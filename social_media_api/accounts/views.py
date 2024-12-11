from django.shortcuts import render, get_object_or_404
from rest_framework import status, views, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .models import CustomUser
from posts.serializers import PostSerializer

User = get_user_model()  # Custom user model

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
'''
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
'''
class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class FollowUser(views.APIView):
    """
    Follow a user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Prevent users from following themselves
        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the following list
        request.user.following.add(user_to_follow)
        return Response({'detail': 'User followed successfully.'}, status=status.HTTP_200_OK)

class UnfollowUser(generics.GenericAPIView):
    """
    Unfollow a user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # Default queryset for all posts

    def post(self, request, user_id, *args, **kwargs):
        """
        Handle unfollowing a user.
        """
        user_to_unfollow = get_object_or_404(User, id=user_id)

        # Prevent users from unfollowing themselves
        if user_to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the following list
        request.user.following.remove(user_to_unfollow)
        
        return Response({'detail': 'User unfollowed successfully.'}, status=status.HTTP_200_OK)

