from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address-list", views.AddressListView.as_view(), name="address-list"),
    path("address", views.AddressView.as_view(), name="address"),
    path("address-form", views.AddressFormView.as_view(), name="address-form"),
]
