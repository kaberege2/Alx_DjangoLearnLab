from django.shortcuts import render
from .models import Post, Comment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters import rest_framework

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
    pagination_class = PostPagination
     # Enable Filtering, Searching, and Ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Define the filter fields
    filterset_fields = ['title', 'created_at']
    
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at']
    ordering = ['title']  # Default ordering by title

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PostPagination
     # Enable Filtering, Searching, and Ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Define the filter fields
    filterset_fields = ['content', 'created_at']
    search_fields = ['content']
    ordering_fields = ['content', 'created_at']
    ordering = ['content']  # Default ordering by title