from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
ORDER_STATUS_CHOICES = [
    ("pending", "pending"),
    ("delivered", "delivered"),
    ("canceled", "canceled"),
]
PAYMENT_STATUS_CHOICES = [
    ("pending", "pending"),
    ("failure", "failure"),
    ("success", "success"),
]


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(
        max_length=255, help_text='A label for your address, e.g., "Home", "Work", etc.'
    )
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField(max_length=300)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField()
    sales = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="review_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="reviews_dislikes", blank=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField(Product)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through="CartItem")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through="OrderItem")
    total_cost = models.PositiveIntegerField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.PositiveIntegerField()


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES)


class PageView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    page_name = models.CharField(max_length=255)


class ClickEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    clicked_element = models.CharField(max_length=255)
