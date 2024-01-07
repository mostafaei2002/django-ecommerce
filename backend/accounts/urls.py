from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="edit-profile"),
    path("address/add/", views.AddAddressView.as_view(), name="add-address"),
    path(
        "address/delete/",
        views.DeleteAddressView.as_view(),
        name="delete-address",
    ),
    path("adderss/edit/<int:id>", views.EditAddressView.as_view(), name="edit-address"),
]
