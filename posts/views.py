from django.shortcuts import get_object_or_404, render

from likes.views import get_client_ip
from posts.models import Post


def post_list(request):
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.visible_objects()
    return render(request, "posts/post_list.html", {
        "posts": posts,
    })


def post_retrieve(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Determine if current user/IP has liked this post
    if request.user.is_authenticated:
        user_has_liked = post.is_liked_by_user(request.user)
    else:
        ip_address = get_client_ip(request)
        user_has_liked = post.is_liked_by_ip(ip_address)

    like_count = post.get_like_count()

    return render(request, "posts/post_retrieve.html", {
        "post": post,
        "like_count": like_count,
        "user_has_liked": user_has_liked,
    })


def about_me(request):
    return render(request, "posts/about_me.html")
