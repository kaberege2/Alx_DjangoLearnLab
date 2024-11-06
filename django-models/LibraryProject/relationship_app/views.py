from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def hello_view(request):
    """A basic function view returning a greeting message."""
    return HttpResponse("Hello, World!")


def book_list(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'book_list': books}  # Create a context dictionary with book list
      return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


#Null view
def list_books(request):
    """A basic function view returning a greeting message."""
    return HttpResponse("Hello, World! = list_books")

#No Redirect to Login Page (No Automatic Login)
#class SignUpView(CreateView):
    
  #  form_class = UserCreationForm
 #   template_name = 'registration/register.html'
 #   success_url = reverse_lazy('login')  # Redirect to login page after successful registration
    
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')  # Redirect to profile page after successful registration

    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Log the user in
        login(self.request, user)

        # Redirect to profile page (or any page you prefer)
        return redirect(self.success_url)

#Null
# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


#Create Role-Based Views: Define views for different roles using the @user_passes_test decorator
# Custom function to check the user's role
# Custom function to check the user's role
def check_role(role):
    def decorator(user):
        # Ensure the user has a userprofile and check their role
        return user.userprofile.role == role if hasattr(user, 'userprofile') else False
    return decorator

@user_passes_test(check_role('Admin'))
def Admin(request):
    return render(request, 'admin_view.html')

@user_passes_test(check_role('Librarian'))
def Librarian(request):
    return render(request, 'librarian_view.html')

@user_passes_test(check_role('Member'))
def Member(request):
    return render(request, 'member_view.html')
