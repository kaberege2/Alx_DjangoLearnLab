## Create a Book
Command:
"Book.objects.create"
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
(No output, but the book is saved in the database)
