from datetime import datetime
from typing import ClassVar
from uuid import uuid4

from django.db import models
from django.urls import reverse

from utils.slug import generate_unique_slug


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    slug = models.CharField(max_length=128, unique=True, db_index=True, blank=True)

    title = models.CharField(max_length=512, blank=True)
    subtitle = models.CharField(max_length=512, blank=True)
    cover_image = models.URLField(blank=True, default="")
    text = models.TextField(blank=True, default="")
    html_cache = models.TextField(blank=True, default="")
    is_raw_html = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, db_index=True)

    og_title = models.CharField(max_length=512, blank=True, default="")
    og_description = models.CharField(max_length=512, blank=True, default="")
    og_image = models.URLField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-created_at"]
        db_table = "posts"

    def __str__(self):
        return self.title

    def save(self, flush_cache=True, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Post, self.title, exclude_pk=self.pk)

        if not self.published_at and self.is_visible:
            self.published_at = datetime.now()

        if flush_cache:
            self.html_cache = ""

        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_retrieve", kwargs={"slug": self.slug})

    def get_like_count(self):
        """Return total number of likes for this post."""
        return self.likes.count()

    def is_liked_by_ip(self, ip_address):
        """Check if this IP address has liked this post."""
        if not ip_address:
            return False
        return self.likes.filter(ip_address=ip_address).exists()

    @classmethod
    def visible_objects(cls):
        return cls.objects.filter(
            is_visible=True,
        ).order_by("-published_at")
