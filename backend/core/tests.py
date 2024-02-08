from accounts.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Review


# Create your tests here.
class CategoryModelTests(TestCase):
    def setUp(self):
        self.parent = Category.objects.create(name="parent", slug="parent")
        self.child = Category.objects.create(
            name="child", slug="child", parent_category=self.parent
        )

    def test_get_items_child_category(self):
        new_product = Product.objects.create(
            categories=self.child, title="something", slug="something", price=2
        )

        parent_products = self.parent.get_all_products()

        self.assertEqual(parent_products, [new_product])


class ProductListViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="cat", slug="cat")
        self.admin = User.objects.create_user(username="admin", password="admin")

    def test_order_by_date(self):
        old_product = Product.objects.create(
            title="p1", slug="p1", categories=self.category, price=10
        )
        new_product = Product.objects.create(
            title="p2", slug="p2", categories=self.category, price=10
        )

        response = self.client.get(reverse("products") + "?order_by=date")

        self.assertEqual(
            list(response.context["product_list"]), [old_product, new_product]
        )

    def test_order_by_rating(self):
        high_rating = Product.objects.create(
            title="p1", slug="p1", categories=self.category, price=10
        )
        low_rating = Product.objects.create(
            title="p2", slug="p2", categories=self.category, price=10
        )

        Review.objects.create(
            rating=5, product=high_rating, user=self.admin, comment="none"
        )

        Review.objects.create(
            rating=1, product=low_rating, user=self.admin, comment="none"
        )

        response = self.client.get(reverse("products") + "?order_by=rating")

        self.assertEqual(
            list(response.context["product_list"]), [high_rating, low_rating]
        )

    def test_order_by_num_ratings(self):
        high_rating = Product.objects.create(
            title="p1", slug="p1", categories=self.category, price=10
        )
        low_rating = Product.objects.create(
            title="p2", slug="p2", categories=self.category, price=10
        )

        Review.objects.create(
            rating=5, product=high_rating, user=self.admin, comment="none"
        )
        Review.objects.create(
            rating=5, product=high_rating, user=self.admin, comment="none"
        )

        Review.objects.create(
            rating=1, product=low_rating, user=self.admin, comment="none"
        )

        response = self.client.get(reverse("products") + "?order_by=num_ratings")

        self.assertEqual(
            list(response.context["product_list"]), [high_rating, low_rating]
        )
