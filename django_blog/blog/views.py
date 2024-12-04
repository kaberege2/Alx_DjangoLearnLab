from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Post
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'blog/home.html')

def user_posts(request):
    posts = Post.objects.all()
    context={"posts": posts}
    #return HttpResponse("Hello world")
    return render(request, 'blog/posts.html', context)

def user_posts_details(request, user_id):
    # Get the user by ID or return a 404 if not found
    user = get_object_or_404(User, id=user_id)
    
    # Get the posts associated with that user
    posts = Post.objects.filter(author=user)
    context = {"user": user, "posts": posts}
    
    # Render the posts to a template
    return render(request, 'blog/posts_details.html', context)

# Register view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            #login(request, form.save())  # Log in the user immediately after registration
            return redirect('login')  # Redirect to the homepage/profile
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})
