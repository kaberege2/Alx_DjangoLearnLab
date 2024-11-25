from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author

# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer