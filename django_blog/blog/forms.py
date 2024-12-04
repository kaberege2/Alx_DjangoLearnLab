from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class CustomUserCreationForm(UserCreationForm):
    # Adding email field to the registration form
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
'''
#Ensure you have templates for listing, viewing, creating, editing, and deleting posts, e.g., post_list.html:
{% for post in posts %}
    <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
    <p>{{ post.content|truncatewords:30 }}</p>
{% endfor %}
'''