from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from app.bot.models import BotUser


@admin.register(BotUser)
class BotUserAdmin(UnfoldModelAdmin):
    list_display = ("telegram_id", 'username', "full_name", "phone_number")
