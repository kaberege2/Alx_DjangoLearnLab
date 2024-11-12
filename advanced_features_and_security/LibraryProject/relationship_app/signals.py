'''
Signal to Automatically Create UserProfile:
Use Django signals to create a UserProfile when a user is created:
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')  # Default role is 'Member'

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    # Create Groups
    editors_group, created = Group.objects.get_or_create(name='Editors')
    viewers_group, created = Group.objects.get_or_create(name='Viewers')

    # Get ContentType for the Book model
    book_content_type = ContentType.objects.get_for_model(Book)

    # Get or create Permissions
    edit_permission = Permission.objects.get(codename='can_edit', content_type=book_content_type)
    view_permission = Permission.objects.get(codename='can_view', content_type=book_content_type)

    # Assign Permissions to Groups
    editors_group.permissions.add(edit_permission)
    viewers_group.permissions.add(view_permission)
