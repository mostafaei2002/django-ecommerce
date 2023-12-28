from django.urls import path

from . import views

urlpatterns = [
    path("accounts/profile/", views.UserProfileView.as_view(), name="profile")
]
