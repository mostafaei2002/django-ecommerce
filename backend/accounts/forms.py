from django import forms
from django.core.validators import RegexValidator

from .models import Address, User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "phone", "bio"]


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "phone",
            "password",
        ]
        widgets = {"password": forms.PasswordInput()}


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["user"]
