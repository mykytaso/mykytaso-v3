from typing import ClassVar

from django import forms

from posts.models import Post
from utils.slug import generate_unique_slug


class PostForm(forms.ModelForm):
    """Front-end post editor.

    The form does not include html_cache (Post.save clears it), view_count (behavioural data), or id / created_at / updated_at (not editable).
    """

    slug = forms.SlugField(
        required=False,
        max_length=128,
        help_text="Leave empty to make it again from the title.",
    )

    class Meta:
        model = Post
        # The groups are the same as PostAdmin.fieldsets.
        fields = (
            # Content
            "title",
            "subtitle",
            "slug",
            "cover_image",
            "text",
            "is_raw_html",
            # Open Graph / Social Media
            "og_title",
            "og_description",
            "og_image",
            # Publishing
            "is_visible",
            "published_at",
        )
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "subtitle": forms.Textarea(attrs={"rows": 2}),
            "text": forms.Textarea(attrs={"rows": 24, "spellcheck": "false"}),
            "og_description": forms.Textarea(attrs={"rows": 3}),
            # The format is necessary to show the value: without it Django writes "Aug. 11, 2026, 2:30 p.m." and the input stays empty.
            # Parsing needs nothing, because DateTimeField.to_python uses parse_datetime, which accepts the ISO "T" separator.
            "published_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        labels: ClassVar[dict[str, str]] = {
            "text": "Body",
            "is_raw_html": "Raw HTML",
            "og_title": "OG title",
            "og_description": "OG description",
            "og_image": "OG image",
        }
        help_texts: ClassVar[dict[str, str]] = {
            "is_raw_html": "Show the body as raw HTML instead of markdown.",
            "published_at": "UTC. If empty, it is set automatically the first time "
            "the post becomes visible.",
        }

    def clean(self):
        """Fill an empty slug here instead of in Post.save().

        Post.save() makes the slug again from a queryset that still contains the
        current slug of this row. Thus, if you clear "my-post" to refresh it, you
        get "my-post-1". Here we can exclude the instance itself.

        This method runs before _post_clean(), thus the new slug still goes
        through Django's uniqueness check.
        """
        cleaned_data = super().clean()

        if cleaned_data.get("slug") or "slug" in self.errors:
            return cleaned_data

        slug = generate_unique_slug(
            Post,
            cleaned_data.get("title", ""),
            exclude_pk=self.instance.pk,
        )
        # A post with no title makes an empty slug, and its get_absolute_url() cannot be reversed.
        # Post.id is a UUID with a default, thus instance.pk exists before the first save.
        cleaned_data["slug"] = slug or f"post-{self.instance.pk.hex[:8]}"

        return cleaned_data
