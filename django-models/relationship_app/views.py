from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView

def hello_view(request):
    """A basic function view returning a greeting message."""
    return HttpResponse("Hello, World!")


def book_list(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'book_list': books}  # Create a context dictionary with book list
      return render(request, 'list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
