from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagField, TagWidget  # Import TagField and TagWidget
from django.forms import widgets  # Add the widgets import here


class CustomUserCreationForm(UserCreationForm):
    # Adding email field to the registration form
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Include tags field in the form

    tags = TagField(widget=TagWidget())  # Use TagWidget for tags field

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']