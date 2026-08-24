import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from likes.models import Like
from markdown.markdown import markdown_text
from posts.decorators import superuser_only
from posts.forms import PostForm, PostImageUploadForm
from posts.models import Post, PostImage
from utils.request import get_client_ip


def post_list(request):
    # order_by() must be explicit: Django does not apply Meta.ordering to a GROUP BY query,
    # and the annotate() below makes this a GROUP BY query.
    queryset = (
        Post.objects.order_by("-created_at")
        if request.user.is_superuser
        else Post.visible_objects()  # already ordered by "-published_at"
    )
    # One COUNT for the full list, in place of one query for each post in the template.
    posts = queryset.annotate(like_count=Count("likes"))

    # One query gives every post this IP likes. The loop then reads the set, and makes no query.
    ip_address = get_client_ip(request)
    liked_post_ids = (
        set(Like.objects.filter(ip_address=ip_address).values_list("post_id", flat=True))
        if ip_address
        else set()
    )
    for post in posts:
        post.user_has_liked = post.id in liked_post_ids

    return render(
        request,
        "posts/post_list.html",
        {
            "posts": posts,
        },
    )


def post_retrieve(request, slug):
    queryset = Post.objects.all() if request.user.is_superuser else Post.visible_objects()
    post = get_object_or_404(queryset, slug=slug)

    # Increment view count atomically, but do not count admin views
    if not request.user.is_superuser:
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
        "Allow: /",
        "",
        f"Sitemap: https://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ---------------------------------------------------------------------------
# Editor (superuser only)
# ---------------------------------------------------------------------------


def _render_preview_html(text, *, is_raw_html):
    """
    Make the HTML for the editor preview.

    The {% render_post %} tag writes to Post.html_cache, but this function does not: the preview must keep nothing.
    is_raw_html is keyword-only, because ruff FBT003 does not permit a boolean positional argument at the call site.
    """

    return text if is_raw_html else markdown_text(text)


def _editor_context(request, form, post=None):
    """
    Make the context for post_form.html, with the preview already rendered.

    upload_form and site_url are here too, because post_form.html includes the image panel.
    The panel needs the same context when htmx swaps it later; see _image_panel().
    """

    return {
        "form": form,
        "post": post,
        "preview_html": _render_preview_html(
            form["text"].value() or "",
            is_raw_html=bool(form["is_raw_html"].value()),
        ),
        "upload_form": PostImageUploadForm(),
        "site_url": request.build_absolute_uri("/").rstrip("/"),
    }


@superuser_only
def editor_guide(request):
    """The writing guide, linked from the editor header."""

    return render(request, "posts/editor_guide.html")


@superuser_only
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post created.")
            # Go back to the editor.
            return redirect("post_update", slug=post.slug)
    else:
        form = PostForm()

    return render(request, "posts/post_form.html", _editor_context(request, form))


@superuser_only
def post_update(request, slug):
    # No visibility filter: only the superuser gets to this view.
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # form.save() calls instance.save() with no arguments, thus flush_cache stays True and html_cache becomes empty.
            # The next page view makes the markdown again.
            post = form.save()
            # The slug can have changed, thus the redirect uses the new one.
            return redirect("post_update", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/post_form.html", _editor_context(request, form, post))


@superuser_only
@require_POST
def post_delete(request, slug):
    """Delete a post."""

    post = get_object_or_404(Post, slug=slug)
    title = post.title
    post.delete()  # Like.post is on_delete=CASCADE, thus the likes go with it

    messages.success(request, f"Post '{title}' deleted.")
    return redirect("post_list")


@superuser_only
@require_POST
def post_preview(request):
    """Make the live preview fragment for the editor. It keeps nothing."""

    html = _render_preview_html(
        request.POST.get("text", ""),
        is_raw_html=request.POST.get("is_raw_html") in {"on", "true", "1"},
    )
    return render(request, "posts/post_preview.html", {"preview_html": html})


# ---------------------------------------------------------------------------
# Post images (superuser only)
# ---------------------------------------------------------------------------


def _image_panel(request, post, upload_form=None):
    """Render the image panel fragment that htmx swaps into #image-panel."""

    return render(
        request,
        "posts/image_panel.html",
        {
            "post": post,
            "upload_form": upload_form or PostImageUploadForm(),
            # The copy button must give an absolute URL: cover_image and og_image are URLFields and refuse a path without a scheme.
            "site_url": request.build_absolute_uri("/").rstrip("/"),
        },
    )


@superuser_only
@require_POST
def post_image_upload(request, slug):
    """Store the uploaded images and return the panel again."""

    post = get_object_or_404(Post, slug=slug)
    form = PostImageUploadForm(request.POST, request.FILES)

    if not form.is_valid():
        return _image_panel(request, post, upload_form=form)

    for file in form.cleaned_data["files"]:
        PostImage.objects.create(post=post, file=file)

    return _image_panel(request, post)


@superuser_only
@require_POST
def post_image_delete(request, slug, image_id):
    """Delete one image of one post. The file goes with it, see posts/signals.py."""

    post = get_object_or_404(Post, slug=slug)
    # The filter takes the post too, thus a wrong pair gives 404 and never deletes an image of another post.
    get_object_or_404(PostImage, id=image_id, post=post).delete()

    return _image_panel(request, post)
