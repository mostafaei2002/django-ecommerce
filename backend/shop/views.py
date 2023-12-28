from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import UserEditForm
from .models import Category, Product, User

# Create your views here.


# Index & Product Views
class IndexView(View):
    def get(self, request):
        top_level_categories = Category.objects.filter(parent_category=None)
        latest_products = Product.objects.all().order_by("-updated_at")[:8]

        # TODO Pass in Top Selling products
        # TODO Pass in some recommended products for logged in users

        return render(
            request,
            "shop/front_page.html",
            {"latest_products": latest_products, "categories": top_level_categories},
        )

    def post(self, request):
        pass


class ProductListView(ListView):
    # Pass in products ordered by top selling by default
    pass


class ProductDetailView(DetailView):
    # Single product Page
    pass


class ProductCategoryListView(ListView):
    pass


# Cart View
class CartView(View):
    pass


# Order Views
class OrderListView(ListView):
    pass


class OrderView(View):
    pass


# User Profile
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        print(request.user.first_name)
        user_form = UserEditForm(
            initial={
                "avatar": request.user.avatar,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "bio": request.user.bio,
            }
        )

        return render(request, "shop/user_profile.html", {"form": user_form})

    def post(self, request):
        user_form = UserEditForm(request.POST)

        if user_form.is_valid():
            user_form.save()

        return render(request, "shop/user_profile.html", {"form": user_form})
