import os
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        objects.filter(author=author)       #To be verified
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"Books by {author.name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print("Author not found.")

# List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        libra = Librarian.objects.get(library= library_name)   #To be verified
        books = library.books.all()
        print(f"Books in {library.name}: {[book.title for book in books]}")
    except Library.DoesNotExist:
        print("Library not found.")

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        libra = Librarian.objects.get(library= library_name)   #To be verified
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print("Library not found.")
    except Librarian.DoesNotExist:
        print("No librarian assigned to this library.")

# Example usage
if __name__ == "__main__":
    get_books_by_author("Author Name")
    get_books_in_library("Library Name")
    get_librarian_for_library("Library Name")
