from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserAccountManager(BaseUserManager):

    def create_user(self, username, email, password=None, **other_fields):
        if not email:
            raise ValueError("Email address is required!")

        email = self.normalize_email(email)

        # Set email verification to False by default (can be overridden in other_fields)
        other_fields.setdefault("is_email_verified", False)

        user = self.model(
            username=username,
            email=email,
            **other_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **other_fields):
        """Create and return a superuser with admin privileges."""
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_email_verified", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128, null=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Email verification fields
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    email_verification_token_created_at = models.DateTimeField(blank=True, null=True)
    pending_email = models.EmailField(blank=True, null=True)

    # Soft delete fields
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    class Meta:
        db_table = "users"

    def generate_verification_token(self):
        """Generate and save a new email verification token."""

        from django.utils import timezone

        from utils.strings import random_verification_token

        self.email_verification_token = random_verification_token()
        self.email_verification_token_created_at = timezone.now()
        self.save(update_fields=[
            "email_verification_token",
            "email_verification_token_created_at",
        ])
        return self.email_verification_token

    def is_verification_token_valid(self, token: str) -> bool:
        """Check if the provided token is valid and not expired."""
        from datetime import timedelta

        from django.conf import settings
        from django.utils import timezone

        # Check if token matches
        if not self.email_verification_token or self.email_verification_token != token:
            return False

        # Check if token is expired (24 hours)
        if not self.email_verification_token_created_at:
            return False

        expiry_hours = getattr(settings, "EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", 24)
        expiry_time = self.email_verification_token_created_at + timedelta(hours=expiry_hours)

        return timezone.now() <= expiry_time

    def verify_email(self):
        """Mark email as verified and clear verification token."""
        self.is_email_verified = True
        self.email_verification_token = None
        self.email_verification_token_created_at = None
        self.save(update_fields=[
            "is_email_verified",
            "email_verification_token",
            "email_verification_token_created_at",
        ])

    def soft_delete(self):
        """Soft delete the user account."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def get_display_name(self):
        """Return username or 'Deleted User' if account is deleted."""
        return "Deleted User" if self.is_deleted else self.username

