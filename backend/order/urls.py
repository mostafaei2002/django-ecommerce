from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.AddOrderView.as_view(), name="add-order"),
    path("<int:id>/", views.OrderDetailView.as_view(), name="order-checkout"),
    path("submit/<int:id>/", views.SubmitOrderView.as_view(), name="submit-order"),
]
