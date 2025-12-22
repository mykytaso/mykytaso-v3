from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from likes.models import Like
from posts.models import Post


def get_client_ip(request):
    """Extract client IP address from request headers."""
    ipaddress = request.META.get("HTTP_X_REAL_IP") \
        or request.META.get("HTTP_X_FORWARDED_FOR") \
        or request.environ.get("REMOTE_ADDR") or ""

    if "," in ipaddress:  # multiple ips in the header
        ipaddress = ipaddress.split(",", 1)[0]
    return ipaddress


@require_POST
def toggle_like(request, slug):
    """Toggle like/unlike for a post. Returns HTMX-compatible HTML fragment."""
    post = get_object_or_404(Post, slug=slug)

    # Get IP address for all users (authenticated and anonymous)
    ip_address = get_client_ip(request)

    if request.user.is_authenticated:
        # Authenticated user flow
        existing_like = Like.objects.filter(post=post, user=request.user).first()

        if existing_like:
            existing_like.delete()
            user_has_liked = False
        else:
            Like.objects.create(post=post, user=request.user, ip_address=ip_address)
            user_has_liked = True
    else:
        # Anonymous user flow (track by IP only)
        existing_like = Like.objects.filter(post=post, ip_address=ip_address, user__isnull=True).first()

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
        request=request
    )
    return HttpResponse(html)
