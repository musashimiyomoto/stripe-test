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

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Order(models.Model):
    items = models.ManyToManyField(Item, through="OrderItem")
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True
    )
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

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
