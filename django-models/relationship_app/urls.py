from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from . import views
from .views import list_books

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
    path('books/', views.book_list, name='books'),
    path('booklist/', list_books, name='bookslist'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]