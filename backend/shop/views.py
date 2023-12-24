from django.shortcuts import render
from django.views import View

from .models import Product

# Create your views here.


class IndexView(View):
    def get(self, request):
        # TODO fetch top_selling products and test
        top_selling_produts = Product.objects.all().order_by("sales")[:10]

        latest_products = Product.objects.all().order_by("created_at")[:10]

        return render(
            request,
            "shop/index.html",
            {
                "top_selling_products": top_selling_produts,
                "latest_products": latest_products,
            },
        )

    def post(request):
        pass
