from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        default="usd",
        choices=[
            ("usd", "USD"),
            ("eur", "EUR"),
            ("rub", "RUB"),
        ],
    )

    def __str__(self):
        return self.name

    def get_display_price(self):
        return f"{self.price} {self.currency.upper()}"


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    # Условия применения скидки
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Минимальная сумма заказа для применения скидки")
    min_items_count = models.PositiveIntegerField(null=True, blank=True, help_text="Минимальное количество товаров для применения скидки")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

    def is_applicable(self, order):
        """Проверяет, можно ли применить скидку к заказу"""
        if not self.is_active:
            return False
        
        # Проверяем минимальную сумму заказа
        if self.min_order_amount:
            order_subtotal = sum(item.get_total_price() for item in order.orderitem_set.all())
            if order_subtotal < self.min_order_amount:
                return False
        
        # Проверяем минимальное количество товаров
        if self.min_items_count:
            total_items = sum(item.quantity for item in order.orderitem_set.all())
            if total_items < self.min_items_count:
                return False
        
        return True


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    # Условия применения налога
    currency = models.CharField(
        max_length=3,
        choices=[
            ("usd", "USD"),
            ("eur", "EUR"),
            ("rub", "RUB"),
        ],
        null=True,
        blank=True,
        help_text="Налог применяется только для указанной валюты"
    )
    is_default = models.BooleanField(default=False, help_text="Налог по умолчанию")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

    def is_applicable(self, order):
        """Проверяет, можно ли применить налог к заказу"""
        if not self.is_active:
            return False
        
        # Проверяем валюту
        if self.currency and self.currency != order.get_currency():
            return False
        
        return True


class Order(models.Model):
    items = models.ManyToManyField(Item, through="OrderItem")
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True
    )
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

    def apply_automatic_tax_and_discount(self):
        """Автоматически применяет подходящие налог и скидку"""
        # Применяем налог
        if not self.tax:
            # Ищем налог для валюты заказа
            applicable_tax = Tax.objects.filter(
                is_active=True,
                currency=self.get_currency()
            ).first()
            
            # Если нет налога для конкретной валюты, берем налог по умолчанию
            if not applicable_tax:
                applicable_tax = Tax.objects.filter(
                    is_active=True,
                    is_default=True
                ).first()
            
            if applicable_tax and applicable_tax.is_applicable(self):
                self.tax = applicable_tax

        # Применяем скидку
        if not self.discount:
            # Ищем все активные скидки и выбираем лучшую
            applicable_discounts = []
            for discount in Discount.objects.filter(is_active=True):
                if discount.is_applicable(self):
                    applicable_discounts.append(discount)
            
            # Выбираем скидку с наибольшим процентом
            if applicable_discounts:
                self.discount = max(applicable_discounts, key=lambda d: d.percent)
        
        self.save()

    def get_total_amount(self):
        total = sum(item.get_total_price() for item in self.orderitem_set.all())

        if self.discount:
            total = total * (1 - self.discount.percent / 100)

        if self.tax:
            total = total * (1 + self.tax.percent / 100)

        return total

    def get_currency(self):
        first_item = self.orderitem_set.first()
        return first_item.item.currency if first_item else "usd"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def get_total_price(self):
        return self.item.price * self.quantity
