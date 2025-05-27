import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemListView(ListView):
    model = Item
    template_name = "payments/item_list.html"
    context_object_name = "items"


class ItemDetailView(DetailView):
    model = Item
    template_name = "payments/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class CreateCheckoutSessionView(View):
    def get(self, request, id, *args, **kwargs):
        item = get_object_or_404(Item, pk=id)
        YOUR_DOMAIN = "http://localhost:8000"
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(item.price * 100),
                            "product_data": {
                                "name": item.name,
                                "description": item.description,
                            },
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=YOUR_DOMAIN + "/success/",
                cancel_url=YOUR_DOMAIN + "/cancel/",
            )
            return JsonResponse({"sessionId": checkout_session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class SuccessView(TemplateView):
    template_name = "payments/success.html"


class CancelledView(TemplateView):
    template_name = "payments/cancel.html"
