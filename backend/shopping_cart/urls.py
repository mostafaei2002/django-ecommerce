from django.urls import path

from . import views

urlpatterns = [
    path("add/<int:id>", views.CartAddView.as_view(), name="add-to-cart"),
    path(
        "delete/<int:id>",
        views.CartDeleteView.as_view(),
        name="delete-from-cart",
    ),
]
