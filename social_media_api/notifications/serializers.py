from rest_framework import serializers
from notifications.models import Notification
from posts.serializers import PostSerializer
from posts.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()  # Custom user model

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Author is a foreign key
    actor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Author is a foreign key
    target = serializers.SerializerMethodField()  # Custom field to serialize 'target'

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'is_read']

    def get_target(self, obj):
        """
        Custom method to serialize the 'target' GenericForeignKey.
        Depending on the content type of the target, we will call the appropriate serializer.
        """
        target_obj = obj.target  # Get the related object based on the GenericForeignKey
        if isinstance(target_obj, Post):  # Check if the target is a Post model
            return PostSerializer(target_obj).data
        # Add other types as necessary, e.g., Comment, User, etc.
        return None  # Or handle other types if needed
