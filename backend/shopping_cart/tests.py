from accounts.models import User
from core.models import Category, Product
from django.test import TestCase
from django.urls import reverse

from .models import Cart

# Create your tests here.


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin")
        self.category = Category.objects.create(name="category", slug="category")

        self.p1 = Product.objects.create(
            title="p1", slug="p1", categories=self.category, price=10
        )
        self.p2 = Product.objects.create(
            title="p2", slug="p2", categories=self.category, price=10
        )

    def test_merge_items_before_login(self):
        self.client.post(reverse("cart"), data={"id": self.p1.id})

        self.client.post(
            reverse("login"), data={"username": "admin", "password": "admin"}
        )

        response = self.client.get(reverse("cart"))
        cart_products = [item.product for item in response.context["cart"].items.all()]

        self.assertEqual(cart_products, [self.p1])

    def test_merge_items_after_login(self):

        self.client.post(
            reverse("login"), data={"username": "admin", "password": "admin"}
        )

        self.client.post(reverse("cart"), data={"id": self.p1.id})

        response = self.client.get(reverse("cart"))
        cart_products = [item.product for item in response.context["cart"].items.all()]

        self.assertEqual(cart_products, [self.p1])

    def test_merge_items_before_after_login(self):

        self.client.post(reverse("cart"), data={"id": self.p1.id})

        self.client.post(
            reverse("login"), data={"username": "admin", "password": "admin"}
        )

        self.client.post(reverse("cart"), data={"id": self.p2.id})

        response = self.client.get(reverse("cart"))
        cart_products = [item.product for item in response.context["cart"].items.all()]

        self.assertEqual(cart_products, [self.p1, self.p2])
