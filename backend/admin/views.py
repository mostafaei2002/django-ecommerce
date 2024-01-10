from django.contrib.auth import logout
from django.shortcuts import redirect, render, reverse
from django.views import View

# Create your views here.


class AdminLogoutView(View):
    def get(self, request):
        logout(request)

        return redirect(reverse("login"))
