from django.urls import path

from . import views

urlpatterns = [
    path("orders/submit", views.OrderView.as_view(), name="submit-order"),
]
