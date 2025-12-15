from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect, get_object_or_404, render

from posts.forms import PostCreateUpdateForm
from posts.models import Post


def post_update(request, post_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostCreateUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_retrieve", post_id=post.id)
    else:
        form = PostCreateUpdateForm(instance=post)

    return render(request, "posts/post_update.html", {
        "form": form,
    })


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PostCreateUpdateForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("post_retrieve", post_id=post.id)
    else:
        form = PostCreateUpdateForm()

    return render(request, "posts/post_create_update.html", {
        "form": form,
    })


def post_list(request):
    posts = Post.visible_objects()
    return render(request, "posts/post_list.html", {
        "posts": posts,
    })


def post_retrieve(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, "posts/post_retrieve.html", {
        "post": post,
    })