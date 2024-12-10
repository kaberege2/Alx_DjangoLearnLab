
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()  # Custom user model

class CustomUserAdmin(UserAdmin):
    model = User  # Tells Django that this admin is for the custom User model
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'bio')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
admin.site.register(User, CustomUserAdmin)

