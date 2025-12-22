from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "post__title", "text")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
