import logging

from django.db import models
from django.db.models import Avg, Count, Sum

logger = logging.getLogger("django")


class CartManager(models.Manager):

    def get_active_cart(self, request):
        if request.user.is_authenticated:
            return self.filter(created_by=request.user, status="active")[0]
        else:
            cart_id = request.session.get("active_cart", None)
            if cart_id:
                active_cart = self.filter(pk=cart_id)[0]
                return active_cart
            else:
                return None

    def get_or_create_active_cart(self, request):
        if request.user.is_authenticated:
            active_cart, status = self.get_or_create(
                created_by=request.user, status="active"
            )
            logger.info(active_cart, status)
            return active_cart
        else:
            active_cart_id = request.session.get("active_cart", None)
            if active_cart_id:
                return self.get(pk=active_cart_id)
            else:
                active_cart = self.create()
                request.session["active_cart"] = active_cart.id
                return active_cart

    def merge_carts(self, request, old_cart):
        # Merge Carts after login
        new_cart = self.get_active_cart(request)
        if not new_cart and old_cart:
            old_cart.set_user(request.user)
        elif new_cart and old_cart:
            old_cart.move_into(new_cart)
