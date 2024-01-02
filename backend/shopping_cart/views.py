from django.shortcuts import render
from django.views import View

# Create your views here.


def handle_carts(request, user):
    # There are 3 scenarios
    # Old Cart && no new cart
    # Old cart && new cart
    # no old cart && new cart
    old_cart_id = request.session.get("active_cart_id")

    # Get old cart
    if old_cart_id:
        old_cart = Cart.objects.get(pk=old_cart_id)
    else:
        old_cart = None

    # Get active cart
    try:
        active_cart = user.carts.get(status="active")
    except Exception:
        active_cart = None

    # Handle carts
    if old_cart and not active_cart:
        old_cart.created_by = user
        old_cart.save()

    elif old_cart and active_cart:
        old_cart_items = old_cart.items.all()

        for item in old_cart_items:
            try:
                existing_active_item = active_cart.items.get(product=item.product)
                existing_active_item.quantity += item.quantity
                existing_active_item.save()
            except Exception:
                new_item = CartItem(
                    product=item.product, quantity=item.quantity, cart=active_cart
                )

        del request.session["active_cart_id"]
        old_cart.delete()


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
        cart_item.delete()

        return redirect(request.META["HTTP_REFERER"])


class CartEditQuantityView(View):
    # TODO Implement interactive quantity modification with vanilla JS
    def post(self, request, id):
        pass
