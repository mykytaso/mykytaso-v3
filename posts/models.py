from typing import ClassVar
from uuid import uuid4

from django.db import models
from django.urls import reverse


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=512, blank=True)
    subtitle = models.CharField(max_length=512, blank=True)
    cover_image = models.URLField(null=True, blank=True)
    text = models.TextField(blank=True)

    is_visible = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_like_count(self):
        """Return total number of likes for this post."""
        return self.likes.count()

    def is_liked_by_user(self, user):
        """Check if authenticated user has liked this post."""
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    def is_liked_by_ip(self, ip_address):
        """Check if anonymous IP address has liked this post."""
        if not ip_address:
            return False
        return self.likes.filter(ip_address=ip_address, user__isnull=True).exists()

    class Meta:
        ordering: ClassVar[list[str]] = ["-created_at"]
        db_table = "posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_retrieve", kwargs={"post_id": self.id})

    @classmethod
    def visible_objects(cls):
        return cls.objects.filter(
            is_visible=True,
        ).order_by("-published_at")
