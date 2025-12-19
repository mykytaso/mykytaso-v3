from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_visible", "published_at", "created_at", "like_count_display"]
    list_filter = ["is_visible", "published_at"]
    search_fields = ["title", "subtitle", "text"]
    readonly_fields = ["id", "created_at", "updated_at"]

    def like_count_display(self, obj):
        return obj.get_like_count()
    like_count_display.short_description = "Likes"
