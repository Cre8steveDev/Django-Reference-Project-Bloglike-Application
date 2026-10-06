from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "category", "body", "cover_image")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Give your idea a clear name"}),
            "category": forms.Select(),
            "body": forms.Textarea(
                attrs={"placeholder": "Begin with the thought you keep returning to..."}
            ),
        }
