from django.urls import path
from .views import RegisterView, LoginView, UserProfileView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # POST /api/accounts/register/
    path('login/', LoginView.as_view(), name='login'),  # POST /api/accounts/login/
    path('profile/', UserProfileView.as_view(), name='profile'),  # GET /api/accounts/profile/
    path('api-token-auth/', views.obtain_auth_token),
]
