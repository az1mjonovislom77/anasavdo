from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from app.user.models import User
from app.user.validations import check_image_size


class Color(models.Model):
    image = models.ImageField(upload_to='images/color/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp']),
        check_image_size
    ])

    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'color'


class Location(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=50, null=True, blank=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    fullAddress = models.TextField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.country)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'notification'


class Currency(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name)
