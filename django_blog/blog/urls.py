from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView, CommentCreateView, CommentUpdateView, CommentDeleteView


urlpatterns = [
    path("home", views.home, name ="home"),
    #path("posts", views.user_posts, name ="posts"),
    #path('user/<int:user_id>/posts/', views.user_posts_details, name='user_posts_details'),
    # Login view url path
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),

    # Logout view url path
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    #User registration path
    path('register/', views.register, name='register'),  
    path('profile/', views.profile, name='user'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
     # CRUD URLs for comments|Comment-related views
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),  # Add comment
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit_comment'),  # Edit comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),  # Delete comment
    path('search/', views.search, name='search'),
     # URL pattern for viewing posts by tag
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
]



