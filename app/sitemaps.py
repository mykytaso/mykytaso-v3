from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from posts.models import Post


class PostSitemap(Sitemap):
    """Sitemap for blog posts."""

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        """Return only visible posts, ordered by publication date."""
        return Post.visible_objects()

    def lastmod(self, obj):
        """Return the last modification time of the post."""
        return obj.published_at or obj.updated_at


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        """Return list of static page URL names."""
        return ["post_list", "about_me"]

    def location(self, item):
        """Return the URL for the static page."""
        return reverse(item)
