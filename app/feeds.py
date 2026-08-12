from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse

from posts.models import Post


class LatestPostsFeed(Feed):
    """RSS feed of the newest visible posts.

    The feed carries the subtitle only, and not the post body. A reader follows the
    link to the site, thus the view count and the like button keep their meaning.
    Rendering the markdown of every post on each request would also be costly,
    because Post.html_cache is empty until the post page is opened.
    """

    title = settings.SITE_NAME
    description = "New posts from mykytaso.com."

    def link(self):
        """Return the page the feed describes. This is not the URL of the feed itself."""
        return reverse("post_list")

    def items(self):
        """Return the 20 newest visible posts. visible_objects() orders by -published_at."""
        return Post.visible_objects()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.subtitle

    def item_pubdate(self, item):
        return item.published_at

    def item_updateddate(self, item):
        return item.updated_at
