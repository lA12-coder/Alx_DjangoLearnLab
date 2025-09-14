from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .models import User
# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserBaseAdmin):
    model=User
    list_display = ('username','email', 'first_name', 'last_name','is_staff', 'date_of_birth')
    fieldsets = UserBaseAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserBaseAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

