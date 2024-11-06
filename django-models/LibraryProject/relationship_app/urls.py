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
    #path('accounts/', include('django.contrib.auth.urls')),    default
     # Login view
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Logout view
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('register/', views.register, name='register'),            #null
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]