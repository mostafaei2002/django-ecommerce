from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import Order, OrderItem

# Create your views here.


class AddOrderView(View):
    def post(self, request):
        # User is authenticated or Is Not
        if request.user.is_authenticated:
            # Turn the active shopping cart into a pending Order
            active_cart = request.user.carts.get(status="active")
            active_cart.status = "ordered"
            active_cart.save()
            active_cart_items = active_cart.items.all()

            new_order = Order(status="pending", user=request.user)
            new_order.save()

            for item in active_cart_items:
                OrderItem.objects.create(
                    price=item.price,
                    quantity=item.quantity,
                    order=new_order,
                    product=item.product,
                )

            # Go to order checkout page where users can see an overview of the order and choose an address
            return redirect(reverse("order-checkout", args=[new_order.id]))
        else:
            return redirect(reverse("register"))


class OrderDetailView(View):
    # If an address is selected redirect to the payments website
    # Otherwise get an address from the user
    def get(self, request, id):
        order_obj = Order.objects.get(pk=id)
        address_list = request.user.addresses.all()

        print("Hello world")
        print(order_obj.user, request.user)
        if order_obj.user != request.user:
            return redirect(reverse("profile"))

        return render(
            request,
            "order/order_detail.html",
            {"order": order_obj, "address_list": address_list},
        )


class SubmitOrderView(View):
    def post(self, request, id):
        # address_id = request.post["address_id"]

        return render(request, "order/payment_placeholder.html")
