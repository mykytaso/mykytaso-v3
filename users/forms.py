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
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]

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
        email = self.cleaned_data["email"]
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
