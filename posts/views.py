from django.db.models import F
from django.shortcuts import get_object_or_404, render

from likes.views import get_client_ip
from posts.models import Post


def post_list(request):
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.visible_objects()

    # Add liked status to each post
    if request.user.is_authenticated:
        for post in posts:
            post.user_has_liked = post.is_liked_by_user(request.user)
    else:
        ip_address = get_client_ip(request)
        for post in posts:
            post.user_has_liked = post.is_liked_by_ip(ip_address)

    return render(request, "posts/post_list.html", {
        "posts": posts,
    })


def post_retrieve(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Increment view count atomically
    Post.objects.filter(slug=slug).update(view_count=F("view_count") + 1)
    post.refresh_from_db()

    # Determine if current user/IP has liked this post
    if request.user.is_authenticated:
        user_has_liked = post.is_liked_by_user(request.user)
    else:
        ip_address = get_client_ip(request)
        user_has_liked = post.is_liked_by_ip(ip_address)

    like_count = post.get_like_count()
    comments = post.comments.select_related("author").all()

    return render(request, "posts/post_retrieve.html", {
        "post": post,
        "like_count": like_count,
        "user_has_liked": user_has_liked,
        "comments": comments,
    })


def about_me(request):
    return render(request, "posts/about_me.html")
