from django.shortcuts import render
from .model import Book

# Create your views here.
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm

def book_list(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.filter(title__icontains=query)  # Safe query
      context = {'book_list': books}  # Create a context dictionary with book list
      return render(request, 'relationship_app/list_books.html', context)


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

["book_list"]