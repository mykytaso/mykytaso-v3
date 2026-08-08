from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from likes.models import Like
from posts.models import Post
from utils.request import get_client_ip


@require_POST
def toggle_like(request, slug):
    """Toggle like/unlike for a post by IP. Returns HTMX-compatible HTML fragment."""
    post = get_object_or_404(Post, slug=slug)

    ip_address = get_client_ip(request)

    existing_like = Like.objects.filter(post=post, ip_address=ip_address).first()

    if existing_like:
        existing_like.delete()
        user_has_liked = False
    else:
        Like.objects.create(post=post, ip_address=ip_address)
        user_has_liked = True

    # Get updated like count and render partial
    like_count = post.get_like_count()
    html = render_to_string(
        "posts/like_button.html",
        {"post": post, "like_count": like_count, "user_has_liked": user_has_liked},
        request=request,
    )
    return HttpResponse(html)
