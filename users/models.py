from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, **other_fields):
        if not email:
            raise ValueError("Email address is required!")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **other_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **other_fields):
        """Create and return a superuser with admin privileges."""
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Admin account. This is a single-author blog, so there is no public sign-up."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128, null=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    class Meta:
        db_table = "users"
