from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrdersView.as_view(), name="orders"),
    path("<int:id>", views.OrdersView.as_view(), name="single-order"),
    path("payment/<int:id>", views.PaymentView.as_view(), name="payment"),
]
