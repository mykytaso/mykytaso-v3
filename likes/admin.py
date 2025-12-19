from django.contrib import admin

from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user", "ip_address", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["post__title", "user__username", "user__email", "ip_address"]
    readonly_fields = ["id", "created_at"]
    raw_id_fields = ["post", "user"]
