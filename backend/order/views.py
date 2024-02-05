from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh
from shopping_cart.models import Cart

from .models import Address, Order, OrderItem

# Create your views here.


class OrdersView(View):
    def get(self, request, id):
        order_obj = Order.objects.get(pk=id)
        address_list = request.user.addresses.all()

        if order_obj.user != request.user:
            return redirect(reverse("profile"))

        return render(
            request,
            "order/order_detail.html",
            {"order": order_obj, "address_list": address_list},
        )

    def post(self, request):
        # User is authenticated or Is Not
        if request.user.is_authenticated:
            # Turn the active shopping cart into a pending Order
            active_cart = Cart.objects.get_active_cart(request)
            new_order = active_cart.submit_order()

            # Go to order checkout page where users can see an overview of the order and choose an address
            messages.success(request, "Order submitted successfully.")
            return HttpResponseClientRedirect(
                redirect_to=reverse("single-order", args=[new_order.id])
            )
        else:
            messages.error(
                request, "Please login/register before submitting your order."
            )
            return HttpResponse(status=204)


class PaymentView(View):
    def post(self, request, id):
        order_obj = Order.objects.get(pk=id)
        address_id = request.POST.get("address")
        if order_obj.user == request.user:
            order_obj.status = "finished"
            order_obj.address = Address.objects.get(pk=address_id)
            order_obj.save()
            messages.success(request, "Payment Unimplemented. Order Submitted")
        return HttpResponseClientRefresh()
