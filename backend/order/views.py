from django.shortcuts import render
from django.urls import reverse
from django.views import View

# Create your views here.


class OrderView(View):
    def post(self, request):
        # User is authenticated or Is Not
        if request.user.is_authenticated:
            # User has an addres or not
            address_list = request.user.addresses
            if len(address_list) > 0:
                return "going to submit"
            else:
                return redirect(reverse("add_address"))
        else:
            return redirect(reverse("register"))
