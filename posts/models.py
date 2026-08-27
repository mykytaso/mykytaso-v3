from datetime import datetime
from pathlib import PurePosixPath
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
    cover_image = models.URLField(
        blank=True,
        default="",
        help_text="Best 1360x765 px (16:9). The post page shows it 680 px wide. "
        "The post list crops it to a centred rectangle.",
    )
    text = models.TextField(blank=True, default="")
    html_cache = models.TextField(blank=True, default="")
    is_raw_html = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, db_index=True)

    og_title = models.CharField(max_length=512, blank=True, default="")
    og_description = models.CharField(max_length=512, blank=True, default="")
    og_image = models.URLField(
        blank=True,
        default="",
        help_text="Best 1200x630 px (1.91:1) — the standard for Open Graph and for "
        "the large Twitter card. Not less than 600x315 px.",
    )

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


def post_image_upload_path(instance, filename):
    """
    Put every image of one post in its own directory, named "<slug>-<uuid8>".

    The name is written one time, at the first upload.
    It does not follow a later slug change: the path of each file is in the database.
    """

    return f"posts/{instance.post.slug}-{instance.post_id.hex[:8]}/{filename}"


class PostImage(models.Model):
    """
    One image uploaded for one post, from the front-end editor.

    The editor gives the absolute URL of the file.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(
        upload_to=post_image_upload_path,
        width_field="width",
        height_field="height",
    )
    # Pillow fills these on save, thus the editor panel shows the size without opening the file again.
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["created_at"]
        db_table = "post_images"

    def __str__(self):
        return self.file.name

    @property
    def filename(self):
        """The name without its directory, for the editor panel.

        Django adds a random suffix when a name repeats,
        thus two uploads of "photo.png" give "photo.png" and "photo_a1b2c3d.png".
        """

        return PurePosixPath(self.file.name).name
