from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_staff", "is_superuser", "is_email_verified", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_email_verified", "created_at")
    search_fields = ("email", "username")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "email_verification_token_created_at")

    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        ("Personal Info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Email Verification", {"fields": ("is_email_verified", "email_verification_token", "email_verification_token_created_at")}),
        ("Important Dates", {"fields": ("created_at", "updated_at", "last_login")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
