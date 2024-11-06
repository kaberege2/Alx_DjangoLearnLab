'''
Signal to Automatically Create UserProfile:
Use Django signals to create a UserProfile when a user is created:
'''
# relationship_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Signal to create a UserProfile whenever a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal to save the UserProfile whenever the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
