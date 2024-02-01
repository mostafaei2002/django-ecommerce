from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


# Extend default User Model
class User(AbstractUser):
    phone = models.CharField(
        validators=[
            RegexValidator("[0-9]+$"),
        ],
        unique=True,
    )
    avatar = models.ImageField(upload_to="avatars", blank=True)

    email_validated = models.BooleanField(default=False)
    phone_validated = models.BooleanField(default=False)

    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(validators=[RegexValidator("[0-9]{5}-[0-9]{5}")])
    address = models.TextField(
        max_length=500, help_text="Enter more description about your address"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
