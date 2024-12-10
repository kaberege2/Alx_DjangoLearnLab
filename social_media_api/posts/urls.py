from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListView, CommentListView, PostViewSet, CommentViewset

router = DefaultRouter()
router.register(r'posts_all', PostViewSet, basename="post-viewset-list" )
router.register(r'comments_all', CommentViewset, basename="comment-viewset-list")

urlpatterns = [
    path("posts_list/", PostListView.as_view(), name="post-generic-list"),
    path("comments_list/", CommentListView.as_view(), name="comments-generic-list"),
    path("", include(router.urls)),
]