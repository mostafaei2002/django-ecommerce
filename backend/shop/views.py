from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import RegisterForm
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


class ProductList(ListView):
    template_name = "shop/product_list.html"
    model = Product
    context_object_name = "products_list"


class ProductView(DetailView):
    template_name = "shop/single_product.html"
    model = Product
    context_object_name = "product"


class LoginView(View):
    def get(self, request):
        return render(request, "shop/login.html")

    def post(self, request):
        pass


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "shop/register.html", {"form": form})

    def post(self, request):
        pass
