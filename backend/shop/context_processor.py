from .models import Cart


def cart_context(request):
    user = request.user

    if user.is_authenticated:
        active_cart = user.carts.get(status="active")
    else:
        active_cart_id = request.session["active_cart_id"]
        active_cart = Cart.objects.get(pk=active_cart_id)

    return {"cart": active_cart}
