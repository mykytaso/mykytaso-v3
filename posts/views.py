from django.shortcuts import get_object_or_404, render

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

    return render(request, "posts/post_retrieve.html", {
        "post": post,
    })


def about_me(request):
    return render(request, "posts/about_me.html")
