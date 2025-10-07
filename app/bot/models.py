from django.db import models
from django.utils import timezone

from app.user.models import User


class BotUser(models.Model):
    telegram_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(max_length=40, null=True, blank=True)
    username = models.CharField(max_length=40, null=True, blank=True)
    tmp_code = models.CharField(max_length=6, null=True, blank=True, unique=True)
    created = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        db_table = 'botuser'
