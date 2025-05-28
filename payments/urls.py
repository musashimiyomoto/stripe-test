from django.urls import path

from .views import (
    AddToOrderView,
    CancelledView,
    CreateCheckoutSessionView,
    CreateOrderCheckoutSessionView,
    ItemDetailView,
    ItemListView,
    OrderDetailView,
    OrderListView,
    SuccessView,
)

urlpatterns = [
    path("", ItemListView.as_view(), name="item_list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("buy/<int:id>/", CreateCheckoutSessionView.as_view(), name="buy_item"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path(
        "buy-order/<int:id>/",
        CreateOrderCheckoutSessionView.as_view(),
        name="buy_order",
    ),
    path("add-to-order/<int:item_id>/", AddToOrderView.as_view(), name="add_to_order"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelledView.as_view(), name="cancel"),
]
