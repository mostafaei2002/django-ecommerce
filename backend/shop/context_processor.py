from .models import Cart


def cart_context(request):
    user = request.user
    active_cart_id = request.session.get("active_cart_id")

    if user.is_authenticated:
        try:
            active_cart = user.carts.get(status="active")
        except Exception:
            return {}

    elif active_cart_id:
        active_cart = Cart.objects.get(pk=active_cart_id)
    else:
        return {}

    return {"cart": active_cart}
