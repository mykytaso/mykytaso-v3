from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from markdown.markdown import markdown_text


register = template.Library()


@register.simple_tag(takes_context=True)
def render_post(context, post):
    if post.is_raw_html:
        html = post.text or post.html_cache # use raw HTML directly, or fall back to cached HTML
    else:
        if not post.html_cache or settings.DEBUG:
            new_html = markdown_text(post.text)

            # Only save if HTML actually changed
            if new_html != post.html_cache:
                post.html_cache = new_html
                post.save(flush_cache=False)

        html = post.html_cache or ""

    return mark_safe(html)
