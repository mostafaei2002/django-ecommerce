from core.models import Product
from django.shortcuts import redirect, render, reverse
from django.views import View

from .models import Cart, CartItem

# Create your views here.


class CartAddView(View):
    # TODO add in user authentication
    def post(self, request, id):
        product_quantity = int(request.POST["quantity"])
        product = Product.objects.get(pk=id)
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

        return redirect(request.META["HTTP_REFERER"])


class CartDeleteView(View):
    # TODO add in user authentication
    def post(self, request, id):
        cart_item = CartItem.objects.get(pk=id)
        if request.user == cart_item.cart.user:
            cart_item.delete()
        else:
            return redirect(reverse("home"))

        return redirect(request.META["HTTP_REFERER"])


class CartEditQuantityView(View):
    # TODO Implement interactive quantity modification with vanilla JS
    def post(self, request, id):
        pass
