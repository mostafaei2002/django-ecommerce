from django import forms
from django.core.validators import MinValueValidator

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment"]


class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(validators=[MinValueValidator], initial=1)
