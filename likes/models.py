from uuid import uuid4

from django.db import models

from posts.models import Post


class Like(models.Model):
    """Track post likes from authenticated users and anonymous IP addresses."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Foreign Keys
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, related_name="likes")

    # IP address tracking (for both authenticated and anonymous users)
    ip_address = models.GenericIPAddressField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "likes"
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                condition=models.Q(user__isnull=False),
                name="unique_authenticated_like"
            ),
            models.UniqueConstraint(
                fields=["post", "ip_address"],
                condition=models.Q(user__isnull=True),
                name="unique_anonymous_like"
            ),
        ]
        indexes = [
            models.Index(fields=["post", "user"]),
            models.Index(fields=["post", "ip_address"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        if self.user:
            return f"{self.user.username} likes {self.post.title}"
        return f"Anonymous ({self.ip_address}) likes {self.post.title}"
