from django import forms
from django.forms import ModelForm

from posts.models import Post


class PostCreateUpdateForm(ModelForm):
    title = forms.CharField(
        label="Title",
        required=True,
    )

    subtitle = forms.CharField(
        label="Subtitle",
        required=False,
    )

    cover_image = forms.URLField(
        label="Cover Image",
        required=False,
    )

    text = forms.CharField(
        label="Text",
        min_length=0,
        max_length=100000,
        required=True,
        widget=forms.Textarea(
            attrs={
                "id": "post-editor",
            }
        ),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "subtitle",
            "cover_image",
            "text",
        ]
