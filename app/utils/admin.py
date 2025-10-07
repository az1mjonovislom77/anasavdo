from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from app.utils.models import Color, Location, Notification, Currency


@admin.register(Color)
class ColorAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ('name', 'image')


@admin.register(Location)
class LocationAdmin(UnfoldModelAdmin):
    list_display = ('id', 'country', 'region', 'created')


@admin.register(Notification)
class NotificationAdmin(UnfoldModelAdmin):
    list_display = ('id', 'user', 'title', 'private', 'created')


@admin.register(Currency)
class CurrencyAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ('id', 'name_uz', 'name_en', 'name_ru')
