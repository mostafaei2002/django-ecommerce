from django.shortcuts import render
from django.views import View

# Create your views here.


class OrderView(View):
    def post(self, request):
        # User is authenticated or Is Not
        if request.user.is_authenticated:
            # User has an addres or not
            pass
        else:
            return redirect("register")
