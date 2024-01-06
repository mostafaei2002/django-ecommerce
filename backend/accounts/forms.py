from django import forms
from django.core.validators import RegexValidator

from .models import Address, User


class UserEditForm(forms.Form):
    avatar = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(validators=[RegexValidator("[0-9]+")])
    bio = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UserEditForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if (
            User.objects.exclude(pk=self.request.user.id)
            .filter(phone=cleaned_data.get("phone"))
            .exists()
        ):
            raise forms.ValidationError("Phone number already exists.")
        return cleaned_data


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


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["user"]
