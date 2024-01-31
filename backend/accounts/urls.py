from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("dashboard", views.ProfileView.as_view(), name="dashboard"),
    path("profile/edit/", views.DashboardView.as_view(), name="profile-edit"),
    path("address/add/", views.AddAddressView.as_view(), name="add-address"),
    path(
        "address/delete/",
        views.DeleteAddressView.as_view(),
        name="delete-address",
    ),
    path("adderss/edit/<int:id>", views.EditAddressView.as_view(), name="edit-address"),
]
