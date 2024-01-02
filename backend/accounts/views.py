from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import UserEditForm, UserRegisterForm
from .models import User

# Create your views here.


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

        return render(request, "accounts/user_profile.html", {"form": user_form})

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
            handle_carts(request, user)
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

        handle_carts(request, user)

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
    pass


class DeleteAddressView(View):
    pass
