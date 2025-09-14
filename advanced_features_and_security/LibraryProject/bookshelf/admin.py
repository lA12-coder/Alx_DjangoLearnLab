from django.contrib import admin
from .models import Book
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .models import CustomUser
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')




class CustomUserAdmin(UserBaseAdmin):
    model=CustomUser
    list_display = ('username','email', 'first_name', 'last_name','is_staff', 'date_of_birth')
    fieldsets = UserBaseAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserBaseAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)