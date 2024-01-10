from django.urls import path

from .views import AdminLogoutView

urlpatterns = [
    path("logout/", AdminLogoutView.as_view(), name="admin-logout"),
]
