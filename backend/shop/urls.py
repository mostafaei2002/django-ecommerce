from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view()),
    path("products/", views.ProductList.as_view(), name="products_list"),
]
