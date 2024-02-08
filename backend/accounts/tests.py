from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import AddressForm, UserRegisterForm
from .models import Address, User


# Create your tests here.
class UserModelTests(TestCase):
    def test_create_login_user(self):
        User.objects.create_user(
            username="admin", password="admin", phone="09104445566"
        )

        self.assertEqual(self.client.login(username="admin", password="admin"), True)

    def test_create_user_wrong_phone_number_self(self):

        register_form = UserRegisterForm(
            {"username": "admin", "password": "admin", "phone": "hello"}
        )
        self.assertEqual(register_form.is_valid(), False)

    def test_login_wrong_password(self):
        User.objects.create_user(
            username="admin", password="admin", phone="09104445566"
        )

        self.assertEqual(
            self.client.login(username="admin", password="not_admin"), False
        )


class AddressModelTests(TestCase):

    def test_add_address_wrong_postal_code(self):
        admin = User.objects.create_user(
            username="admin", password="admin", phone="09104445566"
        )
        address = AddressForm(
            {
                "province": "wa",
                "city": "something",
                "postal_code": "hello wrld",
                "address": "something selse",
                "user": admin,
            }
        )

        self.assertEqual(address.is_valid(), False)


class UserLoginViewTests(TestCase):
    def test_login_view_wrong_password(self):
        User.objects.create_user(
            username="admin", password="admin", phone="09104445566"
        )
        response = self.client.post(
            reverse("login"), {"username": "admin", "password": "wrong_password"}
        )

        self.assertEqual(
            response.headers["Hx-Trigger"],
            '{"messages": [{"message": "Your credentials are invalid.", "tags": "danger"}]}',
        )

        self.assertEqual(
            response.status_code,
            204,
        )

    def test_login_view_correct_password(self):
        User.objects.create_user(
            username="admin", password="admin", phone="09104445566"
        )
        response = self.client.post(
            reverse("login"), {"username": "admin", "password": "admin"}
        )

        self.assertEqual(response.status_code, 200)


class UserDashboardViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="admin")

    def test_profile_view(self):
        self.client.force_login(user=self.admin)
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_dashboard_authorization(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)


class UserLogoutViewTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="admin")

    def test_authorization_after_logout(self):
        self.client.force_login(user=self.admin)
        self.client.post(reverse("logout"))

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
