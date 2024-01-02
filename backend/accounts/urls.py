from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("address/add/", views.AddAddressView.as_view(), name="add-address"),
    path(
        "address/delete/<int:id>",
        views.DeleteAddressView.as_view(),
        name="delete-address",
    ),
    path("adderss/edit/<int:id>", views.EditAddressView.as_view(), name="edit-address"),
]
