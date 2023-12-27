from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


# Extend default User Model
class User(AbstractUser):
    phone = models.CharField(
        validators=[
            MinValueValidator(5),
            MaxValueValidator(15),
            RegexValidator("[0-9]+"),
        ],
        unique=True,
    )
    avatar = models.ImageField(upload_to="avatars")

    email_validated = models.BooleanField(default=False)
    phone_validated = models.BooleanField(default=False)

    bio = models.TextField(max_length=500)


# Product
class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="sub_categories", null=True
    )


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products")
    summary = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=20000, blank=True, null=True)
    price = models.FloatField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )


class Review(models.Model):
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )


# Carts
class Cart(models.Model):
    CART_CHOICES = [
        ("active", "active"),
        ("ordered", "ordered"),
        ("abandoned", "abandoned"),
    ]

    status = models.CharField(choices=CART_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")


class CartItem(models.Model):
    price = models.FloatField(max_length=50)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


# Orders
class Order(models.Model):
    ORDER_STATUS = [("pending", "pending"), ("finished", "finished")]

    status = models.CharField(choices=ORDER_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")


class OrderItem(models.Model):
    price = models.FloatField(max_length=50)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
