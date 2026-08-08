from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from app.sitemaps import PostSitemap, StaticViewSitemap
from likes.views import toggle_like
from posts.views import about_me, post_list, post_retrieve, robots_txt


# Sitemap configuration
sitemaps = {
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}


urlpatterns = [
    # Django admin (the only login on this site)
    path("kerivnyk/", admin.site.urls),
    # Posts app URLs
    path("", post_list, name="post_list"),
    path("posts/<slug:slug>/", post_retrieve, name="post_retrieve"),
    path("posts/<slug:slug>/like/", toggle_like, name="toggle_like"),
    # About me
    path("about/", about_me, name="about_me"),
    # robots.txt
    path("robots.txt", robots_txt, name="robots"),
    # Sitemap
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]
