from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Show these fields in the user list
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_active")
    # Add fields when viewing/editing a user
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )
    # Add fields when creating a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )


# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)


