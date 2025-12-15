# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.html import format_html
#
# from users.models import User
#
#
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """Custom admin for User model with email verification controls."""
#
#     list_display = [
#         "email",
#         "username",
#         "is_email_verified",
#         "email_verified_badge",
#         "is_staff",
#         "is_superuser",
#         "created_at",
#     ]
#
#     list_filter = [
#         "is_email_verified",
#         "is_staff",
#         "is_superuser",
#         "created_at",
#     ]
#
#     search_fields = ["email", "username"]
#
#     ordering = ["-created_at"]
#
#     # Fields to display in user detail/edit page
#     fieldsets = (
#         (None, {"fields": ("email", "username", "password")}),
#         (
#             "Email Verification",
#             {
#                 "fields": (
#                     "is_email_verified",
#                     "email_verification_token",
#                     "email_verification_token_created_at",
#                 ),
#                 "description": (
#                     "Manage email verification status. You can manually verify users "
#                     'by checking "Is email verified".'
#                 ),
#             },
#         ),
#         (
#             "Permissions",
#             {
#                 "fields": ("is_staff", "is_superuser"),
#             },
#         ),
#         (
#             "Important dates",
#             {
#                 "fields": ("last_login", "created_at", "updated_at"),
#             },
#         ),
#     )
#
#     # Fields for creating new user in admin
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "email",
#                     "username",
#                     "password1",
#                     "password2",
#                     "is_email_verified",
#                 ),
#             },
#         ),
#     )
#
#     readonly_fields = ["created_at", "updated_at", "last_login"]
#
#     # Custom actions
#     actions = ["verify_emails", "unverify_emails"]
#
#     def email_verified_badge(self, obj):
#         """Display a colored badge for verification status."""
#         if obj.is_email_verified:
#             return format_html(
#                 '<span style="background-color: #28a745; color: white; padding: 3px 10px; '
#                 'border-radius: 3px;">Verified</span>'
#             )
#         return format_html(
#             '<span style="background-color: #dc3545; color: white; padding: 3px 10px; '
#             'border-radius: 3px;">Unverified</span>'
#         )
#
#     email_verified_badge.short_description = "Status"
#
#     @admin.action(description="Verify selected users")
#     def verify_emails(self, request, queryset):
#         """Bulk action to verify multiple users."""
#         updated = queryset.filter(is_email_verified=False).update(
#             is_email_verified=True,
#             email_verification_token=None,
#             email_verification_token_created_at=None,
#         )
#         self.message_user(request, f"{updated} user(s) verified successfully.")
#
#     @admin.action(description="Unverify selected users")
#     def unverify_emails(self, request, queryset):
#         """Bulk action to unverify multiple users."""
#         updated = queryset.filter(is_email_verified=True).update(
#             is_email_verified=False,
#         )
#         self.message_user(request, f"{updated} user(s) unverified.")
