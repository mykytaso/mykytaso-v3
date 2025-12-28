from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# from django_recaptcha.fields import ReCaptchaField
# from django_recaptcha.widgets import ReCaptchaV2Checkbox


class RegisterForm(UserCreationForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]


class UpdateForm(forms.Form):
    """Form for updating user profile (username and email)."""

    username = forms.CharField(max_length=128, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")

    def __init__(self, *args, **kwargs):
        """Initialize form with current user instance."""
        self.user = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

        # Populate initial values from user instance
        if self.user:
            self.fields["username"].initial = self.user.username
            self.fields["email"].initial = self.user.email

    def clean_username(self):
        """Validate username is unique."""
        username = self.cleaned_data["username"]

        # If username hasn't changed, skip validation
        if self.user and username == self.user.username:
            return username

        # Check if username is already in use by another user
        queryset = get_user_model().objects.filter(username=username)
        if self.user:
            queryset = queryset.exclude(pk=self.user.pk)

        if queryset.exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """Validate email is unique."""
        email = self.cleaned_data["email"]

        # If email hasn't changed, skip validation
        if self.user and email == self.user.email:
            return email

        # Check if email is already in use by another user
        queryset = get_user_model().objects.filter(email=email)
        if self.user:
            queryset = queryset.exclude(pk=self.user.pk)

        if queryset.exists():
            raise forms.ValidationError("This email is already taken.")
        return email


class ResendVerificationForm(forms.Form):
    """Form for resending verification email."""

    email = forms.EmailField(
        label="Email:",
    )
