from django.shortcuts import render
from django.views import View

from .models import Product

# Create your views here.


class IndexView(View):
    def get(self, request):
        top_selling_produts = Product.objects.all()[:10]
        return render(
            request,
            "shop/index.html",
            {
                "top_selling_products": top_selling_produts,
            },
        )

    def post(request):
        pass
