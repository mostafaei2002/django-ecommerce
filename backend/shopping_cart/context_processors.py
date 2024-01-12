from .models import Cart


def cart_context(request):
    user = request.user
    try:
        active_cart_id = request.session.get("active_cart_id")
    except Exception:
        active_cart_id = None

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
