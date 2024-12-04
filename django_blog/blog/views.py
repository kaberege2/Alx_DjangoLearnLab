from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, PostForm
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

def home(request):
    return render(request, 'blog/home.html')
'''
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
'''
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

@login_required
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


# Post List View (List of all blog posts)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# Post Detail View (Single post view)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Post Create View (Create a new post)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

# Post Update View (Update an existing post)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update_form.html'

    def test_func(self):
        # Ensure that the logged-in user is the author of the post
        post = self.get_object()
        return post.author == self.request.user  # Only the author can update the post

    def get_success_url(self):
         # Dynamic success URL: redirect to the updated post's detail page
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

# Post Delete View (Delete a post)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')  # Redirect to post list after deletion

    def test_func(self):
        # Ensure that the logged-in user is the author of the post
        post = self.get_object()
        return post.author == self.request.user  # Only the author can delete the post
