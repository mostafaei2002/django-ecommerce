from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("accounts/profile/", views.UserProfileView.as_view(), name="profile"),
]
