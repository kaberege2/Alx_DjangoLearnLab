from django.contrib import admin
from .models import Book, Author

# Register your models here.
#class AuthorAdmin(admin.ModelAdmin):
admin.site.register(Book)
admin.site.register(Author)