from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline as UnfoldTabularInline

from app.order.models import Order, Item, ItemValue


class ItemInline(UnfoldTabularInline):
    model = Item
    extra = 1


class ItemValueInline(UnfoldTabularInline):
    model = ItemValue
    extra = 1


@admin.register(Order)
class OrderAdmin(UnfoldModelAdmin):
    list_display = ('id', 'user', 'status', 'created', 'price')
    inlines = (ItemInline, )


@admin.register(Item)
class ItemAdmin(UnfoldModelAdmin):
    list_display = ('id', 'order', 'product')
    inlines = (ItemValueInline, )


@admin.register(ItemValue)
class ItemValueAdmin(UnfoldModelAdmin):
    list_display = ('item', 'feature')
