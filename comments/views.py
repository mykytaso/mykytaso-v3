from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from comments.models import Comment
from posts.models import Post


@login_required
def add_comment(request, post_id):
    """Add a comment to a post. Only authenticated users can comment."""
    if request.method != "POST":
        return redirect("post_retrieve", post_id=post_id)

    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get("text", "").strip()

    if not text:
        messages.error(request, "Comment cannot be empty.")
        return redirect("post_retrieve", post_id=post_id)

    Comment.objects.create(
        post=post,
        author=request.user,
        text=text,
    )

    messages.success(request, "Comment added successfully.")
    return redirect("post_retrieve", post_id=post_id)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment. Only the comment author can delete it."""
    if request.method != "POST":
        return redirect("post_list")

    comment = get_object_or_404(Comment, id=comment_id)

    # Only the comment author can delete their comment
    if comment.author != request.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect("post_retrieve", post_id=comment.post.id)

    post_id = comment.post.id
    comment.delete()

    messages.success(request, "Comment deleted successfully.")
    return redirect("post_retrieve", post_id=post_id)
