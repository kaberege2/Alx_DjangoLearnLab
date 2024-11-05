from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
    path('books/', views.book_list, name='books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library'),
]