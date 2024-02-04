import logging

from accounts.models import User
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Q, Sum

from . import managers

logger = logging.getLogger("django")


# Product
class Category(models.Model):
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories")
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    objects = managers.CategoryManager()

    def __str__(self):
        return self.name

    def get_all_products(self):
        products = []
        categories = [self]

        while categories:
            current = categories.pop()

            categories.extend(list(current.children.all()))
            products.extend(list(current.products.all()))

        return products

    def get_subcategories(self):
        categories = [self]
        subcategories = []
        while categories:
            current = categories.pop()
            categories.extend(list(current.children.all()))
            subcategories.extend(list(current.children.all()))

        return subcategories


class Product(models.Model):
    class Meta:
        ordering = ["title"]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="products", default="products/default.png")
    summary = models.TextField(max_length=500, blank=True, null=True)
    description = RichTextField(max_length=20000, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    objects = managers.ProductQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_average_rating(self):
        avg_rating = self.reviews.aggregate(Avg("rating", default=0))["rating__avg"]
        return avg_rating

    # TODO Delete Later
    def get_top_selling():
        top_selling = Product.objects.annotate(
            qty=Sum("order_item__quantity")
        ).order_by("-qty")
        return top_selling


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
