import logging

from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ProductQuantityForm, ReviewForm
from .models import Category, Product


# Create your views here.
class IndexView(View):
    def get(self, request):
        top_level_categories = Category.objects.filter(parent_category=None)
        latest_products = Product.objects.all().order_by("-updated_at")[:8]

        # TODO Pass in Top Selling products
        # TODO Pass in some recommended products for logged in users

        return render(
            request,
            "core/front_page.html",
            {"latest_products": latest_products, "categories": top_level_categories},
        )

    def post(self, request):
        pass


class ProductListView(ListView):
    # Pass in products ordered by top selling by default
    template_name = "core/product_list.html"
    model = Product
    paginate_by = 12
    context_object_name = "product_list"


class ProductDetailView(View):
    def get(self, request, slug):
        # TODO pass in review avg and count
        product = Product.objects.get(slug=slug)
        all_reviews = product.reviews.all()
        review_form = ReviewForm()
        quantity_form = ProductQuantityForm()

        return render(
            request,
            "core/single_product.html",
            {
                "product": product,
                "reviews": all_reviews,
                "review_form": review_form,
                "quantity_form": quantity_form,
            },
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
    template_name = "core/product_list.html"
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
