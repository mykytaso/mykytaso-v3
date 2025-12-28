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


class UpdateForm(forms.ModelForm):
    # Email as a non-model field (won't be auto-saved)
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = get_user_model()
        fields = ["username"]  # Only username is auto-saved

    def __init__(self, *args, **kwargs):
        """Initialize form with current email value."""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["email"].initial = self.instance.email

    def clean_username(self):
        username = self.cleaned_data["username"]
        queryset = (
            get_user_model()
            .objects.filter(username=username)
            .exclude(pk=self.instance.pk)
        )
        if queryset.exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """Validate new email is unique."""
        email = self.cleaned_data["email"]

        # If email hasn't changed, skip validation
        if email == self.instance.email:
            return email

        # Check if email is already in use by another user
        queryset = (
            get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk)
        )
        if queryset.exists():
            raise forms.ValidationError("This email is already taken.")
        return email


class ResendVerificationForm(forms.Form):
    """Form for resending verification email."""

    email = forms.EmailField(
        label="Email:",
    )
