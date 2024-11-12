from django.contrib import admin
from .models import Book
from .models import Author, Book, Library, Librarian, UserProfile
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser 

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
