from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "alex@example.com"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your password"})
    )


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "name",
            "username",
            "email",
            # "birthday",
            # "location",
            # "bio",
            "avatar",
            # "gender",
            # "portfolio_url",
        )
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "yourname"}),
            "email": forms.EmailInput(attrs={"placeholder": "alex@example.com"}),
            "name": forms.TextInput(attrs={"placeholder": "Alex Morgan"}),
            # "birthday": forms.DateInput(attrs={"type": "date"}),
            # "location": forms.TextInput(attrs={"placeholder": "City, Country"}),
            # "bio": forms.Textarea(
            #     attrs={"placeholder": "Tell us a bit about yourself..."}
            # ),
            "avatar": forms.ClearableFileInput(),
            # "gender": forms.Select(),
            # "portfolio_url": forms.URLInput(
            #     attrs={"placeholder": "https://your-site.example"}
            # ),
            "password1": forms.PasswordInput(),
            # "password2": forms.PasswordInput(),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
            "birthday",
            "location",
            "bio",
            "avatar",
            "gender",
            "portfolio_url",
        )
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "yourname"}),
            "email": forms.EmailInput(attrs={"placeholder": "alex@example.com"}),
            "name": forms.TextInput(attrs={"placeholder": "Alex Morgan"}),
            "birthday": forms.DateInput(attrs={"type": "date"}),
            "location": forms.TextInput(attrs={"placeholder": "City, Country"}),
            "bio": forms.Textarea(
                attrs={"placeholder": "Tell us a bit about yourself..."}
            ),
            "avatar": forms.ClearableFileInput(),
            "gender": forms.Select(),
            "portfolio_url": forms.URLInput(
                attrs={"placeholder": "https://your-site.example"}
            ),
        }
