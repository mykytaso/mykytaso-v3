from django.urls import path

from posts.views import post_create, post_list, post_retrieve, post_update
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
    # path("admin/", admin.site.urls),
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
    path("posts/edit/<uuid:post_id>/", post_update, name="post_update"),
    path("posts/create/", post_create, name="post_create"),
]
