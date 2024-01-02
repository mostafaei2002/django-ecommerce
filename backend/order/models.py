from accounts.models import Address, User
from core.models import Product
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


# Orders
class Order(models.Model):
    ORDER_STATUS = [("pending", "pending"), ("finished", "finished")]

    status = models.CharField(choices=ORDER_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


class OrderItem(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
