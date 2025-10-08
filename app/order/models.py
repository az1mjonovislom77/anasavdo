from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from app.product.models import Product, ProductValue, ProductColor
from app.user.models import User
from app.utils.models import Location


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        Pending = "p", "Pending"
        Success = "s", "Success"
        Delivered = "d", "Delivered"
        Cancelled = "c", "Cancelled"

    class ReceieveStatus(models.TextChoices):
        Delivery = "d", "Delivery"
        Pickup = "p", "Pickup"

    class PaymentStatus(models.TextChoices):
        Cash = "cash", "Cash"
        Card = "card", "Card"
        OnlinePayment = "op", "Online Payment"
        OnlineContract = "oc", "Online Contract"

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.Pending)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=40, null=True, blank=True)
    additional_phone_number = models.CharField(max_length=40, null=True, blank=True)
    receive = models.CharField(max_length=20, choices=ReceieveStatus.choices)
    payment = models.CharField(max_length=20, choices=PaymentStatus.choices)
    price = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created']


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, blank=True, null=True)

    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.order} for {self.product}"

    class Meta:
        db_table = 'item'


class ItemValue(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    feature = models.ForeignKey(ProductValue, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item} | {self.feature}"

    class Meta:
        db_table = 'itemvalue'
        verbose_name = 'Item value'
        verbose_name_plural = 'Item values'
