from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Review, User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "phone", "bio"]


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password",
            "confirm_password",
        ]
        widgets = {"password": forms.PasswordInput()}

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
