import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .models import Discount, Item, Order, OrderItem, Tax


STRIPE_KEYS = {
    "usd": {
        "publishable": settings.STRIPE_PUBLISHABLE_KEY,
        "secret": settings.STRIPE_SECRET_KEY,
    },
    "eur": {
        "publishable": (
            settings.STRIPE_PUBLISHABLE_KEY_EUR
            if hasattr(settings, "STRIPE_PUBLISHABLE_KEY_EUR")
            else settings.STRIPE_PUBLISHABLE_KEY
        ),
        "secret": (
            settings.STRIPE_SECRET_KEY_EUR
            if hasattr(settings, "STRIPE_SECRET_KEY_EUR")
            else settings.STRIPE_SECRET_KEY
        ),
    },
    "rub": {
        "publishable": (
            settings.STRIPE_PUBLISHABLE_KEY_RUB
            if hasattr(settings, "STRIPE_PUBLISHABLE_KEY_RUB")
            else settings.STRIPE_PUBLISHABLE_KEY
        ),
        "secret": (
            settings.STRIPE_SECRET_KEY_RUB
            if hasattr(settings, "STRIPE_SECRET_KEY_RUB")
            else settings.STRIPE_SECRET_KEY
        ),
    },
}


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
        currency = self.object.currency
        context["STRIPE_PUBLISHABLE_KEY"] = STRIPE_KEYS[currency]["publishable"]
        return context


class CreateCheckoutSessionView(View):
    def get(self, request, id, *args, **kwargs):
        item = get_object_or_404(Item, pk=id)
        currency = item.currency

        stripe.api_key = STRIPE_KEYS[currency]["secret"]

        YOUR_DOMAIN = request.build_absolute_uri("/")
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": currency,
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
                success_url=YOUR_DOMAIN + "success/",
                cancel_url=YOUR_DOMAIN + "cancel/",
            )
            return JsonResponse({"id": checkout_session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class CreateOrderCheckoutSessionView(View):
    def get(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, pk=id)
        
        # Проверяем, что заказ принадлежит текущей сессии
        if order.session_key != request.session.session_key:
            return JsonResponse({"error": "Unauthorized access to order"}, status=403)
        
        # Автоматически применяем подходящие налог и скидку
        order.apply_automatic_tax_and_discount()
        
        currency = order.get_currency()

        stripe.api_key = STRIPE_KEYS[currency]["secret"]

        YOUR_DOMAIN = request.build_absolute_uri("/")

        try:
            line_items = []

            for order_item in order.orderitem_set.all():
                line_items.append(
                    {
                        "price_data": {
                            "currency": currency,
                            "unit_amount": int(order_item.item.price * 100),
                            "product_data": {
                                "name": order_item.item.name,
                                "description": order_item.item.description,
                            },
                        },
                        "quantity": order_item.quantity,
                    }
                )

            session_data = {
                "line_items": line_items,
                "mode": "payment",
                "success_url": YOUR_DOMAIN + "success/",
                "cancel_url": YOUR_DOMAIN + "cancel/",
            }

            discounts = []
            if order.discount:
                coupon = stripe.Coupon.create(
                    percent_off=float(order.discount.percent),
                    duration="once",
                    name=order.discount.name,
                )
                discounts.append({"coupon": coupon.id})

            if discounts:
                session_data["discounts"] = discounts

            if order.tax:
                tax_rate = stripe.TaxRate.create(
                    display_name=order.tax.name,
                    percentage=float(order.tax.percent),
                    inclusive=False,
                )
                session_data["line_items"] = [
                    {**item, "tax_rates": [tax_rate.id]} for item in line_items
                ]

            checkout_session = stripe.checkout.Session.create(**session_data)
            return JsonResponse({"id": checkout_session.id})

        except Exception as e:
            return JsonResponse({"error": str(e)})


class OrderListView(ListView):
    model = Order
    template_name = "payments/order_list.html"
    context_object_name = "orders"
    ordering = ["-created_at"]
    
    def get_queryset(self):
        # Фильтруем заказы только для текущей сессии
        if not self.request.session.session_key:
            self.request.session.create()
        
        return Order.objects.filter(
            session_key=self.request.session.session_key
        ).order_by("-created_at")


class OrderDetailView(DetailView):
    model = Order
    template_name = "payments/order_detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        # Получаем заказ только если он принадлежит текущей сессии
        obj = super().get_object(queryset)
        if obj.session_key != self.request.session.session_key:
            from django.http import Http404
            raise Http404("Order not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = self.object.get_currency()
        context["STRIPE_PUBLISHABLE_KEY"] = STRIPE_KEYS[currency]["publishable"]
        
        # Показываем, какие налоги и скидки будут применены при оплате
        temp_order = Order.objects.get(pk=self.object.pk)
        temp_order.apply_automatic_tax_and_discount()
        context["preview_tax"] = temp_order.tax
        context["preview_discount"] = temp_order.discount
        context["preview_total"] = temp_order.get_total_amount()
        
        return context


class AddToOrderView(View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        quantity = int(request.POST.get("quantity", 1))

        # Убеждаемся, что у сессии есть ключ
        if not request.session.session_key:
            request.session.create()

        order_id = request.session.get("order_id")
        if order_id:
            try:
                order = Order.objects.get(pk=order_id, session_key=request.session.session_key)
            except Order.DoesNotExist:
                order = Order.objects.create(session_key=request.session.session_key)
                request.session["order_id"] = order.id
        else:
            order = Order.objects.create(session_key=request.session.session_key)
            request.session["order_id"] = order.id

        order_item, created = OrderItem.objects.get_or_create(
            order=order, item=item, defaults={"quantity": quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        # Сбрасываем налог и скидку, чтобы они пересчитались при следующем просмотре
        order.tax = None
        order.discount = None
        order.save()

        messages.success(request, f"{item.name} добавлен в заказ!")
        return redirect("item_detail", pk=item_id)


class SuccessView(TemplateView):
    template_name = "payments/success.html"


class CancelledView(TemplateView):
    template_name = "payments/cancel.html"
