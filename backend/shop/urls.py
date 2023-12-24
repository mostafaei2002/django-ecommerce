from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view()),
    path("products/", views.ProductList.as_view(), name="products_list"),
    path("product/<slug:slug>", views.ProductView.as_view(), name="single_product"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
