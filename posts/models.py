from typing import ClassVar
from uuid import uuid4

from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=512, blank=True)
    subtitle = models.CharField(max_length=512, blank=True)
    text = models.TextField(blank=True)
    html_cache = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)
    is_commentable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self):
        return self.title
