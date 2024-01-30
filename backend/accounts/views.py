import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect
from shopping_cart.models import Cart

from . import forms
from .models import Address, User

# Create your views here.
logger = logging.getLogger("django")


def merge_carts(request, user):
    # There are 3 scenarios
    # Old Cart && no new cart
    # Old cart && new cart
    # no old cart && new cart
    old_cart_id = request.session.get("active_cart_id")

    # Get old cart
    if old_cart_id:
        old_cart = Cart.objects.get(pk=old_cart_id)
    else:
        old_cart = None

    # Get active cart
    try:
        active_cart = user.carts.get(status="active")
    except Exception:
        active_cart = None

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
    def get(self, request):
        user_form = forms.UserEditForm(instance=request.user)

        address_list = request.user.addresses.all()
        orders = request.user.orders.all()

        return render(
            request,
            "accounts/user_dashboard.html",
            {
                "form": user_form,
                "address_list": address_list,
                "orders": orders,
            },
        )


class ProfileEditView(LoginRequiredMixin, View):
    def post(self, request):
        user_form = forms.UserEditForm(
            request.POST, request.FILES, instance=request.user
        )

        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Your profile was updated successfully.")
            return redirect(reverse("profile"))

        address_list = request.user.addresses.all()
        orders = request.user.orders.all()

        messages.error(request, "Invalid inputs.")
        return render(
            request,
            "accounts/user_profile.html",
            {
                "form": user_form,
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
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
                username=username,
                email=form_data["email"],
                phone=form_data["phone"],
                password=password,
            )
            # Login registered user & handle cart logic
            user = authenticate(request, username=username, password=password)
            merge_carts(request, user)
            if user is not None:
                login(request, user)
                messages.success("Account created successfully.")
                return HttpResponseClientRedirect(reverse("home"))

        return render(
            request, "accounts/register_form.html", {"register_form": register_form}
        )


class UserLoginView(View):
    def get(self, request):
        return render(request, "accounts/login_form.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("home"))

        # Login & Merge old cart with new Cart
        login_form = AuthenticationForm()
        username = request.POST.get("username")

        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        merge_carts(request, user)

        if user is not None:
            login(request, user)

            messages.success(request, "You are Logged in.")
            return HttpResponseClientRedirect(redirect_to=reverse("home"))
        else:
            login_form = AuthenticationForm({"username": username, "password": ""})
            return HttpResponse("<p class='text-danger mb-0'>Credentials Invalid!</p>")


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You are logged out.")
        return redirect(reverse("home"))


class AddAddressView(LoginRequiredMixin, View):
    def get(self, request):
        address_form = AddressForm()
        return render(request, "accounts/add_address.html", {"form": address_form})

    def post(self, request):
        address_form = AddressForm(request.POST)

        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()

            messages.success(request, "Address added successfully.")
            return redirect(reverse("profile"))

        return render(request, "accounts/add_address.html", {"form": address_form})


class DeleteAddressView(LoginRequiredMixin, View):
    def post(self, request):
        address_id = request.POST["address_id"]
        address = Address.objects.get(pk=address_id)
        address.delete()

        messages.success(request, "Address deleted successfully.")
        return redirect("profile")


class EditAddressView(View):
    pass
