from django import forms
from django.contrib.auth.models import User

from .models import Review, User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "phone", "bio"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
