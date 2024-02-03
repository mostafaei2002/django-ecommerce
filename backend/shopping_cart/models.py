from accounts.models import User
from core.models import Product
from django.core.validators import MinValueValidator
from django.db import models


# Carts
class Cart(models.Model):
    CART_CHOICES = [
        ("active", "active"),
        ("ordered", "ordered"),
        ("abandoned", "abandoned"),
    ]

    status = models.CharField(choices=CART_CHOICES, default="active", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="carts", null=True
    )

    def calculate_total(self):
        return self.items.all().aggregate(models.Sum("price"))["price__sum"]


class CartItem(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} {self.product}"

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        super().save(*args, **kwargs)


# Create your models here.
