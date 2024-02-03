from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("products/", views.ProductListView.as_view(), name="products_page"),
    path(
        "products/<slug:slug>",
        views.ProductDetailView.as_view(),
        name="single_product",
    ),
    path("search/", views.SearchViewList.as_view(), name="search"),
]
