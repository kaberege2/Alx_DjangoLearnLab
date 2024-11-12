from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.
 ["class CustomUser(AbstractUser):", "date_of_birth", "profile_photo"]
 ["class CustomUserManager(BaseUserManager):"]

class BookModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()


class Authore(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Authore, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        ]

    def __str__(self):
        return self.title

class Librarys(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Books, related_name='libraries')

    def __str__(self):
        return self.name

class Librarians(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Librarys, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name

class CustomUsers(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
        
#define a UserProfile with a role field:
class UserProfiles(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class CustomUserManagers(BaseUserManager):
    def create_users(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superusers(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

