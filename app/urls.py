from django.contrib import admin
from django.urls import path

from comments.views import add_comment, delete_comment
from likes.views import toggle_like
from posts.views import about_me, post_list, post_retrieve
from users.views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetRequestView,
    CustomPasswordResetSetNewView,
    RegisterView,
    ResendVerificationView,
    UserDetailView,
    UserUpdateView,
    VerifyEmailView,
)


urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # User authentication URLs
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("accounts/me/", UserDetailView.as_view(), name="user_profile"),
    path("accounts/me/update/", UserUpdateView.as_view(), name="user_update"),
    path(
        "accounts/me/password_change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),

    # Email verification URLs
    path(
        "accounts/verify/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path(
        "accounts/resend-verification/",
        ResendVerificationView.as_view(),
        name="resend_verification",
    ),

    # Password reset URLs
    path(
        "accounts/password-reset/",
        CustomPasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        CustomPasswordResetSetNewView.as_view(),
        name="password_reset_set_new",
    ),

    # Posts app URLs
    path("", post_list, name="post_list"),
    path("posts/<uuid:post_id>/", post_retrieve, name="post_retrieve"),
    path("posts/<uuid:post_id>/like/", toggle_like, name="toggle_like"),

    # Comments app URLs
    path("comments/<uuid:post_id>/add/", add_comment, name="add_comment"),
    path("comments/<uuid:comment_id>/delete/", delete_comment, name="delete_comment"),

    # About me
    path("about/", about_me, name="about_me"),
]
