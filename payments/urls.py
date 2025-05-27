from django.urls import path

from .views import (
    CancelledView,
    CreateCheckoutSessionView,
    ItemDetailView,
    ItemListView,
    SuccessView,
)

urlpatterns = [
    path("", ItemListView.as_view(), name="item_list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path(
        "buy/<int:id>/",
        CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelledView.as_view(), name="cancel"),
]
