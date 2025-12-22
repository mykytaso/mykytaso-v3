from uuid import uuid4

from django.db import models


class Comment(models.Model):
    """User comments on posts. Only authenticated users can comment."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Foreign Keys
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="comments")

    # Content
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"{self.author.username} on {self.post.title}"
