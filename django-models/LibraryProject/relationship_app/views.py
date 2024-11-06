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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm  # Assuming you have a BookForm for handling book creation and editing

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
#For clarity and to avoid potential confusion or conflicts, 
#I recommend using descriptive view function names such as admin_view, librarian_view, and member_view
def check_role(role):
    def decorator(user):
        # Ensure the user has a userprofile and check their role
        return user.userprofile.role == role if hasattr(user, 'userprofile') else False
    return decorator

@login_required
@user_passes_test(check_role('Admin'))
def Admin(request):
    return render(request, 'admin_view.html')

@login_required
@user_passes_test(check_role('Librarian'))
def Librarian(request):
    return render(request, 'librarian_view.html')

@login_required
@user_passes_test(check_role('Member'))
def Member(request):
    return render(request, 'member_view.html')


# Add a new book (requires 'can_add_book' permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')  # Redirect to the list of books after adding
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

# Edit an existing book (requires 'can_change_book' permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')  # Redirect after editing
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})

# Delete a book (requires 'can_delete_book' permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')  # Redirect after deletion
    return render(request, 'confirm_delete.html', {'book': book})
