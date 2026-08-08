from uuid import uuid4

from django.db import models

from posts.models import Post


class Like(models.Model):
    """Track post likes by anonymous IP address."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Foreign Keys
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    # IP address tracking (one like per IP per post)
    ip_address = models.GenericIPAddressField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "likes"
        constraints = (
            models.UniqueConstraint(
                fields=["post", "ip_address"],
                name="unique_like_per_ip",
            ),
        )
        indexes = (models.Index(fields=["post", "ip_address"]),)
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.ip_address} likes {self.post.title}"
