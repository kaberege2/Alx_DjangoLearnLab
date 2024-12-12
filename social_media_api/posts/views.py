from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Like
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from rest_framework import  filters, status, views, generics, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework
from rest_framework.exceptions import PermissionDenied
from posts.serializers import LikeSerializer
from rest_framework.exceptions import NotFound
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response

# Create your views here.

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostPagination(PageNumberPagination):
    page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
     # Enable Filtering, Searching, and Ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Define the filter fields
    filterset_fields = ['title', 'created_at']
    
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'title', 'created_at']
    ordering = ['id']  # Default ordering by title

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Check if the user is the author before updating
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You can only update your own posts!")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is the author before deleting
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts!")
        instance.delete()

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    #permission_classes = [IsAuthenticated]
    pagination_class = PostPagination
     # Enable Filtering, Searching, and Ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Define the filter fields
    filterset_fields = ['content', 'created_at']
    search_fields = ['content']
    ordering_fields = ['id', 'content', 'created_at']
    ordering = ['id']  # Default ordering by title

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Check if the user is the author before updating
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You can only update your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is the author before deleting
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()

class UserFeed(generics.GenericAPIView):
    """
    Get posts from the users that the current user follows.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination
    serializer_class = PostSerializer
    #queryset = CustomUser.objects.all()  # Default queryset for all posts

    def get_queryset(self):
        """
        Return the posts from the users the current user follows.
        """
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        """
        Handle the GET request and return paginated posts.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ''''  # Check if the user has already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        like = Like.objects.create(user=request.user, post=post)
        '''
        post = get_object_or_404(Post, id=pk)

         # Try to get the existing like, or create it if it doesn't exist
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post owner (author)
        Notification.objects.create(
            recipient=post.author,  # The author of the post receives the notification
            actor=request.user,     # The user who liked the post
            verb='liked your post', # The action being performed (liking the post)
            target=post,            # The target of the action (the post itself)
            target_content_type=ContentType.objects.get_for_model(Post),  # The content type for the post model
            target_object_id=post.id,  # The ID of the post
        )

        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

class UnlikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        
        post = get_object_or_404(Post, id=pk)
        # Check if the user has liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        # Optionally, create a notification that the like was removed
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='unliked your post',
            target=post,
            target_content_type=ContentType.objects.get_for_model(Post),
        )

        return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)