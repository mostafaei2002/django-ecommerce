from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("products", views.ProductListView.as_view(), name="products"),
    path(
        "products/<slug:slug>",
        views.ProductDetailView.as_view(),
        name="single-product",
    ),
]
