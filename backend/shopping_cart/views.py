from core.models import Product
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views import View

from .models import Cart

# Create your views here.


class CartView(View):
    def get(self, request):
        active_cart = Cart.objects.get_active_cart(request)

        return render(
            request, "shopping_cart/partials/cart.html", {"cart": active_cart}
        )

    def post(self, request):
        obj_id = request.POST.get("id", None)
        product_quantity = request.POST.get("quantity", 1)
        product = Product.objects.get(pk=obj_id)

        if obj_id and product_quantity:
            active_cart = Cart.objects.get_or_create_active_cart(request)
            active_cart.add_item(product, int(product_quantity))

            messages.success(request, "Product added to cart successfully.")
            return HttpResponse(status=204)
        else:
            messages.error(request, "Failed to add product to cart.")
            return HttpResponse(status=400)

    def put(self, request):
        pass

    def delete(self, request):
        obj_id = request.GET.get("id", 0)
        active_cart = Cart.objects.get_active_cart(request)
        try:
            active_cart.delete_item(obj_id)
            messages.success(request, "Cart item deleted successfully.")
        except Exception:
            messages.error(request, "Item Doesn't exist")
            return HttpResponse(status=400)

        return render(
            request, "shopping_cart/partials/cart.html", {"cart": active_cart}
        )
