from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path(
        "categories/<slug:slug>/",
        views.ProductCategoryListView.as_view(),
        name="category",
    ),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "products/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="single_product",
    ),
    path("accounts/profile/", views.UserProfileView.as_view(), name="profile"),
]
