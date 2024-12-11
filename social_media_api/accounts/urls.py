from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, FollowUser, UnfollowUser
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # POST /api/accounts/register/
    path('login/', LoginView.as_view(), name='login'),  # POST /api/accounts/login/
    path('profile/', UserProfileView.as_view(), name='profile'),  # GET /api/accounts/profile/
    path('api-token-auth/', views.obtain_auth_token),
    path('follow/<int:user_id>/', FollowUser.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUser.as_view(), name='unfollow_user'),
]
