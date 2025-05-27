from django.urls import path
from .views import ItemDetailView, CreateCheckoutSessionView, SuccessView, CancelledView

urlpatterns = [
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('buy/<int:id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelledView.as_view(), name='cancel'),
]
