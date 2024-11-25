from django.urls import path, include
from .views import BookList,  AuthorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'authors_all', AuthorViewSet, basename='author-list')

urlpatterns = [
    path('books_all/', BookList.as_view(), name="book_list"),
    path("", include(router.urls))
]