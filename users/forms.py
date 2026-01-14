from typing import ClassVar

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordMixin, UsernameField
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class LoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "light",
                "data-size": "normal",
                "class": "custom-recaptcha-class",
            }
        )
    )


class RegisterForm(SetPasswordMixin, forms.ModelForm):
    """Form for registering a new user."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["autofocus"] = True

    # Honeypot field - should remain empty
    website = forms.CharField(
        required=False,
        label="Website (leave blank)",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "class": "honeypot-field",
                "aria-hidden": "true",
            }
        ),
    )

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "light",
                "data-size": "normal",
                "class": "custom-recaptcha-class",
            }
        )
    )

    password1, password2 = SetPasswordMixin.create_password_fields()

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
        field_classes: ClassVar[dict[str, type]] = {"username": UsernameField}

    def clean_website(self):
        """Reject submission if honeypot field is filled (indicates bot)."""
        website = self.cleaned_data.get("website")
        if website:
            # Silently fail - don't reveal that this is a honeypot
            raise forms.ValidationError("")
        return website

    def clean(self):
        self.validate_passwords()
        return super().clean()

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        self.validate_password_for_user(self.instance)

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        if commit and hasattr(self, "save_m2m"):
            self.save_m2m()
        return user


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
