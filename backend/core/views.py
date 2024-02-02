import logging

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh

from .forms import ProductQuantityForm, ReviewForm
from .models import Category, Product

logger = logging.getLogger("django")


# Create your views here.
class IndexView(View):
    def get(self, request):
        top_level_categories = Category.objects.filter(parent_category=None)
        latest_products = Product.objects.all().order_by("-updated_at")[:8]
        top_selling = Product.get_top_selling()

        return render(
            request,
            "core/front_page.html",
            {
                "latest_products": latest_products,
                "top_selling": top_selling,
                "categories": top_level_categories,
            },
        )


class ProductListView(ListView):
    # Pass in products ordered by top selling by default
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
        product = Product.objects.get(slug=slug)
        review_form = ReviewForm(request.POST)
        rating = request.POST.get("rating")

        if review_form.is_valid() and rating:
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.rating = rating
            new_review.product = product
            messages.success(request, "Review added successfully.")
            new_review.save()

            return HttpResponseClientRefresh()

        if not rating:
            messages.error(request, "Please rate the product.")

        messages.error(request, "Please enter a comment")

        return HttpResponse(status=204)


class SearchViewList(ListView):
    template_name = "search/search_list.html"
    paginate_by = 10
    context_object_name = "product_list"

    def get_queryset(self):
        query = self.request.GET["query"]
        return Product.objects.all().filter(
            Q(title__contains=query) | Q(description__contains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET["query"]
        return context
