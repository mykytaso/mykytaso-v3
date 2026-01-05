from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_visible", "published_at", "created_at", "like_count_display"]
    list_filter = ["is_visible", "published_at"]
    search_fields = ["title", "subtitle", "text", "og_title", "og_description"]
    readonly_fields = ["id", "created_at", "updated_at"]

    fieldsets = [
        (
            "Content",
            {
                "fields": [
                    "slug",
                    "title",
                    "subtitle",
                    "cover_image",
                    "text",
                    "is_raw_html",
                    "html_cache",
                ]
            },
        ),
        (
            "Open Graph / Social Media",
            {
                "fields": ["og_title", "og_description", "og_image"],
                "description": "Meta tags for social media sharing (Twitter, Facebook, etc.)",
            },
        ),
        (
            "Publishing",
            {
                "fields": ["is_visible", "published_at", "view_count"],
            },
        ),
        (
            "Metadata",
            {
                "fields": ["id", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    def like_count_display(self, obj):
        return obj.get_like_count()
    like_count_display.short_description = "Likes"
