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
    path("carts/add/<int:id>", views.CartAddView.as_view(), name="add-to-cart"),
    path(
        "carts/delete/<int:id>",
        views.CartDeleteView.as_view(),
        name="delete-from-cart",
    ),
    path("orders/submit", views.OrderView.as_view(), name="submit-order"),
    path("accounts/register/", views.UserRegisterView.as_view(), name="register"),
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/profile/", views.UserProfileView.as_view(), name="profile"),
]
