from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from likes.models import Like
from likes.views import get_client_ip
from users.forms import RegisterForm, ResendVerificationForm, UpdateForm
from utils.email import MailgunError, send_password_reset_email, send_verification_email


User = get_user_model()


class RegisterView(CreateView):
    """User registration view."""

    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """Save the user and send verification email."""
        # Create user (will be unverified by default)
        response = super().form_valid(form)
        user = self.object

        # Generate verification token
        token = user.generate_verification_token()

        # Build verification URL
        verification_url = self.request.build_absolute_uri(
            reverse("verify_email", kwargs={"token": token})
        )

        # Try to send verification email
        try:
            send_verification_email(user, verification_url)
            messages.success(
                self.request,
                "Registration successful! Please check your email to verify your account.",
            )
        except MailgunError:
            # Email failed, but account was created
            messages.warning(
                self.request,
                "Account created, but I couldn't send the verification email. "
                "Please request a new verification email.",
            )
            # Redirect to resend verification page instead
            self.success_url = reverse("resend_verification")

        return response


class CustomLoginView(LoginView):
    """Custom login view."""

    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Check email verification before allowing login."""
        user = form.get_user()

        # Check if email is verified
        if not user.is_email_verified:
            messages.error(
                self.request,
                "Your email isn't verified. Please check your inbox to complete verification.",
            )
            # Add link to resend verification
            messages.info(
                self.request,
                f'<a href="{reverse("resend_verification")}">Click here</a> '
                "to resend the verification email.",
                extra_tags="safe",
            )
            return self.form_invalid(form)

        # Get user's IP address before login
        user_ip = get_client_ip(self.request)

        # Log the user in
        response = super().form_valid(form)

        # Migrate anonymous likes from this IP to authenticated user
        if user_ip:

            # Find anonymous likes from this IP address
            anonymous_likes = Like.objects.filter(
                ip_address=user_ip,
                user__isnull=True
            )

            # For each anonymous like, check if user already liked this post
            for like in anonymous_likes:
                # Check if user already has a like for this post
                user_already_liked = Like.objects.filter(
                    post=like.post,
                    user=user
                ).exists()

                if not user_already_liked:
                    # Migrate the anonymous like to the user (preserve IP address)
                    like.user = user
                    like.save()
                else:
                    # User already liked this post, delete the duplicate anonymous like
                    like.delete()

        return response

    def get_success_url(self):
        """Redirect to next URL if provided, otherwise to user profile."""
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse_lazy("user_profile")


class CustomLogoutView(LogoutView):
    """Custom logout view."""

    next_page = reverse_lazy("post_list")

    def dispatch(self, request, *args, **kwargs):
        """Add logout message before redirecting."""
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "You have been successfully logged out.")
        return response


class UserDetailView(LoginRequiredMixin, TemplateView):
    """User profile view."""

    template_name = "users/user_profile.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        """Add user to context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """User profile update view."""

    template_name = "users/user_profile_update.html"
    form_class = UpdateForm
    success_url = reverse_lazy("user_profile")
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        """Return the current user."""
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Custom password change view."""

    template_name = "users/password_change.html"
    success_url = reverse_lazy("login")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        """Change password, log out user, and show success message."""
        super().form_valid(form)
        messages.success(
            self.request,
            "Your password has been changed successfully! Please log in with your new password.",
        )
        logout(self.request)
        return redirect(self.success_url)


class VerifyEmailView(TemplateView):
    """Handle email verification from token link."""

    # template_name = "users/email_verified.html"

    def get(self, request, *args, **kwargs):
        """Process verification token."""
        token = kwargs.get("token")

        # Find user with this token
        try:
            user = User.objects.get(email_verification_token=token)
        except User.DoesNotExist:
            # Token doesn't exist or already used
            messages.error(request, "Invalid verification link.")
            return redirect("login")

        # Check if already verified
        if user.is_email_verified:
            messages.info(request, "Email already verified. You can log in.")
            return redirect("login")

        # Validate token (check expiry)
        if user.is_verification_token_valid(token):
            # Token is valid, verify the user
            user.verify_email()

            # Get user's IP address before login
            user_ip = get_client_ip(request)

            # Log the user in automatically
            login(request, user)

            # Migrate anonymous likes from this IP to authenticated user
            if user_ip:
                # Find anonymous likes from this IP address
                anonymous_likes = Like.objects.filter(
                    ip_address=user_ip,
                    user__isnull=True
                )

                # For each anonymous like, check if user already liked this post
                for like in anonymous_likes:
                    # Check if user already has a like for this post
                    user_already_liked = Like.objects.filter(
                        post=like.post,
                        user=user
                    ).exists()

                    if not user_already_liked:
                        # Migrate the anonymous like to the user (preserve IP address)
                        like.user = user
                        like.save()
                    else:
                        # User already liked this post, delete the duplicate anonymous like
                        like.delete()

            messages.success(request, "Email verified successfully! You are now logged in.")
            return redirect("user_profile")
        # Token expired
        messages.error(
            request,
            "Verification link has expired. Please request a new verification email.",
        )
        return redirect("resend_verification")


class ResendVerificationView(FormView):
    """Allow users to request a new verification email."""

    template_name = "users/resend_verification.html"
    form_class = ResendVerificationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """Send new verification email."""
        email = form.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists (security)
            messages.success(
                self.request,
                "A verification link has been sent.",
            )
            return super().form_valid(form)

        # Check if already verified
        if user.is_email_verified:
            messages.info(self.request, "This email is already verified. You can log in.")
            return redirect("login")

        # Generate new token (replaces old one)
        token = user.generate_verification_token()

        # Build verification URL
        verification_url = self.request.build_absolute_uri(
            reverse("verify_email", kwargs={"token": token})
        )

        # Send email
        try:
            send_verification_email(user, verification_url)
            messages.success(
                self.request,
                "A verification link has been sent.",
            )
        except MailgunError:
            messages.error(
                self.request,
                "Failed to send verification email. Please try again later.",
            )

        return super().form_valid(form)


class CustomPasswordResetRequestView(PasswordResetView):
    """Custom password reset view with Mailgun email."""

    template_name = "users/password_reset_request.html"
    success_url = reverse_lazy("password_reset_request")

    def form_valid(self, form):
        """Send password reset email using Mailgun."""
        email = form.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists (security)
            messages.success(
                self.request,
                "If this email is in the system, a reset link has been sent. It’s valid for 1 hour.",
            )
            return redirect(self.success_url)

        # Generate password reset token using Django's built-in token generator
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build password reset URL
        reset_url = self.request.build_absolute_uri(
            reverse("password_reset_set_new", kwargs={"uidb64": uid, "token": token})
        )

        # Send email using Mailgun
        try:
            send_password_reset_email(user, reset_url)
            messages.success(
                self.request,
                "If this email is in the system, a reset link has been sent. It’s valid for 1 hour.",
            )
        except MailgunError:
            messages.error(
                self.request,
                "Failed to send password reset email. Please try again later.",
            )

        return redirect(self.success_url)


class CustomPasswordResetSetNewView(PasswordResetConfirmView):
    """Custom password reset confirm view."""

    template_name = "users/password_reset_set_new.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """Add success message when password is reset."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Your password has been reset successfully! You can now log in with your new password.",
        )
        return response
