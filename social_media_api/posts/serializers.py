
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model
User = get_user_model()  # Custom user model

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Author is a foreign key
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content",  "created_at", "updated_at", "comments"]
