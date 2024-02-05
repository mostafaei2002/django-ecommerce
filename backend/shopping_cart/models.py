from accounts.models import User
from core.models import Product
from django.contrib import messages
from django.core.validators import MinValueValidator
from django.db import models

from . import managers


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

    objects = managers.CartManager()

    def calculate_total(self):
        return self.items.all().aggregate(models.Sum("price"))["price__sum"]

    def add_item(self, product, quantity):

        item, created = CartItem.objects.get_or_create(cart=self, product=product)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()

    def delete_item(self, id):
        try:
            item = self.items.get(pk=id)
            item.delete()
        except Exception as e:
            raise e

    def set_user(self, user):
        self.created_at = user
        self.save()

    def move_into(self, new_cart):
        items = self.items.all()
        for item in items:
            item.cart = new_cart
            item.save()

        self.delete()


class CartItem(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} {self.product}"

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        super().save(*args, **kwargs)
