import logging
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.http import HttpResponse, QueryDict
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_htmx.http import (
    HttpResponseClientRedirect,
    HttpResponseClientRefresh,
    trigger_client_event,
)
from shopping_cart.models import Cart, CartItem

from . import forms
from .models import Address, User

# Create your views here.
logger = logging.getLogger("django")


def merge_carts(request, user):
    # There are 3 scenarios
    # Old Cart && no new cart
    # Old cart && new cart
    # no old cart && new cart
    old_cart_id = request.session.get("active_cart_id", None)

    # Get old cart
    old_cart = Cart.objects.get(pk=old_cart_id)

    # Get active cart
    active_cart = user.carts.get(status="active")
    logger.info(old_cart, active_cart)

    # Handle carts
    if old_cart and not active_cart:
        old_cart.created_by = user
        old_cart.save()

    elif old_cart and active_cart:
        old_cart_items = old_cart.items.all()

        for item in old_cart_items:
            try:
                existing_active_item = active_cart.items.get(product=item.product)
                existing_active_item.quantity += item.quantity
                existing_active_item.save()
            except Exception:
                new_item = CartItem(
                    product=item.product, quantity=item.quantity, cart=active_cart
                )

        del request.session["active_cart_id"]
        old_cart.delete()


class ProfileView(LoginRequiredMixin, View):
    def put(self, request):
        data = BytesIO(request.body)
        self.PUT, self.FILES = request.parse_file_upload(request.META, data)
        user_form = forms.UserEditForm(self.PUT, self.FILES, instance=request.user)

        if not user_form.changed_data:
            messages.error(request, "Please change your data then submit.")
            return HttpResponse(status=204)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Profile updated successfully.")

            return HttpResponseClientRefresh()

        messages.error(request, "Invalid inputs.")
        return render(
            request, "accounts/includes/edit_profile.html", {"profile_form": user_form}
        )


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = forms.UserEditForm(instance=request.user)

        address_list = request.user.addresses.all()
        orders = request.user.orders.all()

        return render(
            request,
            "accounts/user_dashboard_page.html",
            {
                "profile_form": user_form,
                "address_list": address_list,
                "orders": orders,
            },
        )


class UserRegisterView(View):
    def get(self, request):
        register_form = forms.UserRegisterForm()
        return render(
            request, "accounts/register_form.html", {"register_form": register_form}
        )

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("home"))

        register_form = forms.UserRegisterForm(request.POST)

        if register_form.is_valid():
            form_data = register_form.clean()
            username = form_data["username"]
            password = form_data["password"]

            new_user = User.objects.create_user(
                username=username,
                phone=form_data["phone"],
                password=password,
            )
            # Login registered user & handle cart logic
            user = authenticate(request, username=username, password=password)
            merge_carts(request, user)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created successfully.")
                return HttpResponseClientRedirect(reverse("home"))

        return render(
            request, "accounts/register_form.html", {"register_form": register_form}
        )


class UserLoginView(View):
    def get(self, request):
        return render(request, "accounts/login_form.html")

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseClientRedirect(redirect_to=reverse("home"))

        # Login & Merge old cart with new Cart
        login_form = AuthenticationForm()
        username = request.POST.get("username")
        password = request.POST.get("password")

        old_cart = Cart.objects.get_active_cart(request)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            Cart.objects.merge_carts(request, old_cart)

            messages.success(request, "You are Logged in.")
            return HttpResponseClientRedirect(redirect_to=reverse("home"))
        else:
            login_form = AuthenticationForm({"username": username, "password": ""})
            messages.error(request, "Your credentials are invalid.")
            return HttpResponse(status=204)


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You are logged out.")
        return redirect(reverse("home"))


class AddressFormView(LoginRequiredMixin, View):
    def get(self, request):
        address_form = forms.AddressForm()
        return render(
            request, "accounts/address_form.html", {"address_form": address_form}
        )

    def post(self, request):
        obj_id = request.POST["id"]
        obj = Address.objects.get(pk=obj_id)
        address_form = forms.AddressForm(instance=obj)
        return render(
            request,
            "accounts/address_edit_form.html",
            {"address_form": address_form, "address_id": obj_id},
        )


class AddressListView(LoginRequiredMixin, View):
    def get(self, request):
        address_list = request.user.addresses.all()
        return render(
            request,
            "accounts/includes/address_list.html",
            {"address_list": address_list},
        )


# Manage Single Addresses
class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        address_form = forms.AddressForm(request.POST)

        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()

            messages.success(request, "Address added successfully.")
            address_list = request.user.addresses.all()
            return render(
                request,
                "accounts/includes/address_list.html",
                {"address_list": address_list},
            )

        messages.error(request, "Please enter a valid address.")
        return render(
            request, "accounts/address_form.html", {"address_form": address_form}
        )

    def put(self, request):
        data = QueryDict(request.body)
        obj_id = data.get("address_id")
        logger.info(obj_id)

        obj = Address.objects.get(pk=obj_id)
        address_form = forms.AddressForm(data, instance=obj)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, "Address updated successfully")

            address_list = request.user.addresses.all()
            return render(
                request,
                "accounts/includes/address_list.html",
                {"address_list": address_list},
            )

        messages.error(request, "Failed to update address. Invalid input.")
        return render(
            request, "accounts/address_edit_form.html", {"address_form": address_form}
        )

    def delete(self, request):
        data = QueryDict(request.body)
        obj_id = data.get("id")
        obj = Address.objects.get(pk=obj_id)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, "Adderss deleted successfully.")
            address_list = request.user.addresses.all()
            return render(
                request,
                "accounts/includes/address_list.html",
                {"address_list": address_list},
            )
        else:
            messages.error(request, "You're not authorized.")
            return HttpResponse(status=204)
