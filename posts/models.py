from typing import ClassVar
from uuid import uuid4

from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=512, blank=True)
    subtitle = models.CharField(max_length=512, blank=True)
    cover_image = models.URLField(blank=True)
    text = models.TextField(blank=True)

    is_visible = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self):
        return self.title

    @classmethod
    def visible_objects(cls):
        return cls.objects.filter(
            is_visible=True,
        ).order_by("-published_at")