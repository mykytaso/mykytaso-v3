import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from posts.models import Post
from utils.request import get_client_ip


def post_list(request):
    posts = Post.objects.all() if request.user.is_superuser else Post.visible_objects()

    # Add liked status to each post
    ip_address = get_client_ip(request)
    for post in posts:
        post.user_has_liked = post.is_liked_by_ip(ip_address)

    return render(
        request,
        "posts/post_list.html",
        {
            "posts": posts,
        },
    )


def post_retrieve(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Increment view count atomically
    Post.objects.filter(slug=slug).update(view_count=F("view_count") + 1)
    post.refresh_from_db()

    # Determine if the current IP has liked this post
    ip_address = get_client_ip(request)
    user_has_liked = post.is_liked_by_ip(ip_address)

    like_count = post.get_like_count()

    return render(
        request,
        "posts/post_retrieve.html",
        {
            "post": post,
            "like_count": like_count,
            "user_has_liked": user_has_liked,
        },
    )


def about_me(request):
    start_date = date(2023, 8, 7)
    today = datetime.datetime.now().date()
    delta = relativedelta(today, start_date)
    return render(request, "posts/about_me.html", {"delta": delta})


def robots_txt(request):
    """Generate robots.txt dynamically."""
    lines = [
        "User-agent: *",
        f"Sitemap: https://{request.get_host()}/sitemap.xml",
        "Disallow: /kerivnyk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
