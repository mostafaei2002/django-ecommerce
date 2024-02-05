import logging

from django.contrib import messages
from django.core.paginator import Paginator
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
        latest_products = Product.objects.all().order_by("-updated_at")[:6]
        top_selling = Product.objects.all().order_items("sales")[:6]

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
    def get(self, request):
        # Get queries
        query = request.GET.get("query", "")
        order_by = request.GET.get("order_by", "")
        category_slug = request.GET.get("category", "")
        page = int(request.GET.get("page", 1))
        next_page = page + 1

        top_level_categories = Category.objects.get_top_level_categories()

        logger.info(
            f"Query: {query} category: {category_slug} ordered by {order_by} page {page} next_page {next_page}"
        )

        # Handle Queries
        products = Product.objects.all()

        if query:
            products = products.filter(
                Q(title__contains=query) | Q(summary__contains=query)
            )

        if category_slug:
            category_obj = Category.objects.get(slug=category_slug)
            tareget_categories = [category_obj, *category_obj.get_subcategories()]
            products = products.filter(categories__in=tareget_categories)

        if order_by:
            products = products.order_items(order_by)

        # Pagination
        product_paginator = Paginator(products, 12)
        if page > product_paginator.num_pages:
            return HttpResponse(status=204)
        elif page == product_paginator.num_pages:
            next_page = None
            products = product_paginator.page(page).object_list
        else:
            products = product_paginator.page(page).object_list

        # Choose Template
        if request.htmx and request.htmx.trigger != "search":
            template_name = "core/includes/product_list.html"
        else:
            template_name = "core/products_page.html"

        return render(
            request,
            template_name,
            {
                "product_list": products,
                "next_page": next_page,
                "query": query,
                "top_level_categories": top_level_categories,
                "category_slug": category_slug,
                "order_by": order_by,
            },
        )


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
