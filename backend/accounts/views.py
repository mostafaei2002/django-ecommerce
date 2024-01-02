from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import AddressForm, UserEditForm, UserRegisterForm
from .models import Address, User

# Create your views here.


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


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(
            initial={
                "avatar": request.user.avatar,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "bio": request.user.bio,
            }
        )

        address_list = request.user.addresses.all()

        return render(
            request,
            "accounts/user_profile.html",
            {"form": user_form, "address_list": address_list},
        )

    def post(self, request):
        user_form = UserEditForm(request.POST)

        if user_form.is_valid():
            user_form.save()

        return render(request, "accounts/user_profile.html", {"form": user_form})


class UserRegisterView(View):
    def get(self, request):
        register_form = UserRegisterForm()

        return render(request, "accounts/register.html", {"form": register_form})

    def post(self, request):
        register_form = UserRegisterForm(request.POST)

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
                return redirect(reverse("profile"))

        return render(request, "accounts/register.html", {"form": register_form})


class UserLoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        # breakpoint()
        return render(request, "accounts/login.html", {"form": login_form})

    def post(self, request):
        # Login & Merge old cart with new Cart
        login_form = AuthenticationForm()
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        merge_carts(request, user)

        if user is not None:
            login(request, user)

            return redirect(reverse("profile"))
        else:
            login_form = AuthenticationForm({"username": username, "password": ""})
            return render(
                request,
                "accounts/login.html",
                context={"form": login_form, "error": "Your credentials are invalid."},
            )


class AddAddressView(View):
    def get(self, request):
        address_form = AddressForm()
        return render(request, "accounts/add_address.html", {"form": address_form})

    def post(self, request):
        address_form = AddressForm(request.POST)

        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect(reverse("profile"))

        return render(request, "accounts/add_address.html", {"form": address_form})


class DeleteAddressView(View):
    pass


class EditAddressView(View):
    pass
