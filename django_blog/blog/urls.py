from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path("home", views.my_test, name ="home"),
    path("posts", views.my_test, name ="posts"),
    # Login view url path
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout view url path
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    #User registration path
    path('register/', views.register, name='register'),  
    path('profile/', views.profile, name='user'),
]