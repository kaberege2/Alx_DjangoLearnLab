from django.urls import path, include
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, AuthorViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'authors_all', AuthorViewSet, basename='author-list')

urlpatterns = [
    path("books/", BookListView.as_view(), name='book-list'),  # List all books
    path("books/<int:pk>/", BookDetailView.as_view(), name='book-detail'),  # Retrieve a specific book by ID
    path("books/create/", BookCreateView.as_view(), name='book-create'),  # Create a new book
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name='book-update'),  # Update an existing book
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name='book-delete'),  # Delete a book
    path("books/update/", BookUpdateView.as_view(), name='book-update'),  # Update existing books
    path("books/delete/", BookDeleteView.as_view(), name='book-delete'),  # Delete  books
    path("", include(router.urls)),
    path('api-token-auth/', obtain_auth_token),  #Set up an endpoint to retrieve authentication tokens using DRF’s obtain_auth_token view.
]