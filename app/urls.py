from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from app.feeds import LatestPostsFeed
from app.sitemaps import PostSitemap, StaticViewSitemap
from likes.views import toggle_like
from posts.views import (
    about_me,
    editor_guide,
    post_create,
    post_delete,
    post_image_delete,
    post_image_upload,
    post_list,
    post_preview,
    post_retrieve,
    post_update,
    robots_txt,
)


# Sitemap configuration
sitemaps = {
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}


urlpatterns = [
    # Django admin (the only login on this site)
    path("kerivnyk/", admin.site.urls),
    # Logout, for the navbar button (superuser only).
    path("logout/", LogoutView.as_view(next_page="post_list"), name="logout"),
    # Posts app URLs
    path("", post_list, name="post_list"),
    # Editor (superuser only).
    path("editor/new/", post_create, name="post_create"),
    path("editor/preview/", post_preview, name="post_preview"),
    path("editor/guide/", editor_guide, name="editor_guide"),
    path("posts/<slug:slug>/edit/", post_update, name="post_update"),
    path("posts/<slug:slug>/delete/", post_delete, name="post_delete"),
    # Image panel of the editor. These live under posts/, not editor/, because they act on an existing post, exactly like edit/ and delete/ above.
    # editor/ is only for routes that have no post to act on.
    # The slug comes first, thus they do not shadow posts/<slug:slug>/.
    path("posts/<slug:slug>/images/", post_image_upload, name="post_image_upload"),
    path(
        "posts/<slug:slug>/images/<uuid:image_id>/delete/",
        post_image_delete,
        name="post_image_delete",
    ),
    path("posts/<slug:slug>/", post_retrieve, name="post_retrieve"),
    path("posts/<slug:slug>/like/", toggle_like, name="toggle_like"),
    # About me
    path("about/", about_me, name="about_me"),
    # robots.txt
    path("robots.txt", robots_txt, name="robots"),
    # Sitemap
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    # RSS feed
    path("rss.xml", LatestPostsFeed(), name="rss"),
]


# Development only. In production DEBUG is False and nginx serves /media/ straight
# from disk, thus Django never sends the file bytes.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
