from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


# TODO add helper functions to models
# Extend default User Model
class User(AbstractUser):
    phone = models.CharField(
        validators=[
            RegexValidator("[0-9]+"),
        ],
        unique=True,
    )
    avatar = models.ImageField(upload_to="avatars")

    email_validated = models.BooleanField(default=False)
    phone_validated = models.BooleanField(default=False)

    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username


# Product
class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories")
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="products")
    summary = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=20000, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.title


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

    def __str__(self):
        return f"{self.user} on {self.product}"


# Carts
class Cart(models.Model):
    CART_CHOICES = [
        ("active", "active"),
        ("ordered", "ordered"),
        ("abandoned", "abandoned"),
        ("logged_in", "logged_in"),
    ]

    status = models.CharField(choices=CART_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="carts", null=True
    )


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


# Orders
class Order(models.Model):
    ORDER_STATUS = [("pending", "pending"), ("finished", "finished")]

    status = models.CharField(choices=ORDER_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")


class OrderItem(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
