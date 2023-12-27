from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

# Create your views here.


# Index & Product Views
class IndexView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ProductListView(ListView):
    pass


class ProductCategoryListView(ListView):
    pass


class ProductDetailView(DetailView):
    pass


# Cart View
class CartView(View):
    pass


# Orders
class OrderListView(ListView):
    pass


class OrderView(View):
    pass


# User Profile
class UserProfileView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
