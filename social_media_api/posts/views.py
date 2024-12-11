from django.shortcuts import render
from .models import Post, Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters import rest_framework
from rest_framework.exceptions import PermissionDenied

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
    permission_classes = [IsAuthenticated]
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