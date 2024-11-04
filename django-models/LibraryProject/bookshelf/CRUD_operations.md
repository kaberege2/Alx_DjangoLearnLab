## Create a Book
```python
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
#(No output, but the book is saved in the database)

## Retrieve the Book
Command:
Book.objects.all()
#<QuerySet [<Book: 1984>]>

## Update the Book's Title
Command:
book.title = "Nineteen Eighty-Four"
book.save()
#(No output, but the book title is updated)

## Delete the Book
Command:
book.delete()
#(No output, but the book is deleted)



