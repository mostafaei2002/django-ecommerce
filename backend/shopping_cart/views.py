from core.models import Product
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views import View

from .models import Cart, CartItem

# Create your views here.


class CartView(View):
    def get(self, request):
        user = request.user
        try:
            active_cart_id = request.session.get("active_cart_id")
        except Exception:
            active_cart_id = None

        if user.is_authenticated:
            try:
                active_cart = user.carts.get(status="active")
            except Exception:
                return render(request, "shopping_cart/partials/cart.html", {})

        elif active_cart_id:
            active_cart = Cart.objects.get(pk=active_cart_id)
        else:
            return render(request, "shopping_cart/partials/cart.html", {})

        return render(
            request, "shopping_cart/partials/cart.html", {"cart": active_cart}
        )

    def post(self, request):
        obj_id = request.POST.get("id")
        product_quantity = int(request.POST["quantity"])
        product = Product.objects.get(pk=obj_id)
        user = request.user

        # Get the active cart for authenticated and non-authenticated users
        if user.is_authenticated:
            try:
                active_cart = user.carts.get(status="active")
            except Exception:
                active_cart = Cart(created_by=user, status="active")
                active_cart.save()

        else:
            active_cart_id = request.session.get("active_cart_id")
            if active_cart_id:
                active_cart = Cart.objects.get(pk=active_cart_id)
            else:
                active_cart = Cart(status="active")
                active_cart.save()
                request.session["active_cart_id"] = active_cart.id

        # Add quantity if cart item already is in cart
        try:
            cart_item = active_cart.items.get(product=product)
            cart_item.quantity += product_quantity

        except Exception:
            cart_item = CartItem(
                product=product,
                quantity=product_quantity,
                cart=active_cart,
            )

        cart_item.save()
        messages.success(request, "Product added to cart successfully.")

        return HttpResponse(status=204)

    def put(self, request):
        pass

    def delete(self, request):
        obj_id = request.GET.get("id")
        cart_item = CartItem.objects.get(pk=obj_id)
        if request.user == cart_item.cart.created_by:
            cart_item.delete()
            messages.success(request, "Cart item deleted successfully.")
        else:
            messages.error(request, "You are not authorized. Please Login.")
            return HttpResponse(status=204)

        active_cart_id = request.session.get("active_cart_id", None)

        if active_cart_id:
            active_cart = Cart.objects.get(pk=active_cart_id)
        else:
            active_cart = request.user.carts.get(status="active")

        return render(
            request, "shopping_cart/partials/cart.html", {"cart": active_cart}
        )
