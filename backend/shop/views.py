from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ReviewForm, UserEditForm
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
    template_name = "shop/product_list.html"
    model = Product
    paginate_by = 12
    context_object_name = "product_list"


class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        all_reviews = product.reviews.all()
        review_form = ReviewForm()

        return render(
            request,
            "shop/single_product.html",
            {"product": product, "reviews": all_reviews, "review_form": review_form},
        )

    def post(self, request, slug):
        user = self.request.user
        product = Product.objects.get(slug=slug)
        review_form = ReviewForm(self.request.POST)

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = user
            new_review.product = product
            new_review.save()

        return redirect("single_product", slug=slug)


class ProductCategoryListView(ListView):
    template_name = "shop/product_list.html"
    paginate_by = 10
    context_object_name = "product_list"

    def get_queryset(self):
        self.slug = self.kwargs["slug"]
        return Product.objects.filter(
            Q(categories__slug=self.slug)
            | Q(categories__parent_category__slug=self.slug)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.slug
        return context


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
