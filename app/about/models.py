from django.core.validators import FileExtensionValidator
from django.db import models
from app.user.validations import validate_phone_number, check_image_size


class OurContact(models.Model):
    address = models.CharField(max_length=255)
    phone_numbers = models.JSONField()
    emails = models.JSONField()
    working_time = models.TextField()

    def __str__(self):
        return self.address[:30]


class News(models.Model):
    class NewsType(models.TextChoices):
        products = 'p', 'products'
        services = 's', 'services'
        technology = 't', 'technology'
        company = 'c', 'company'

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255, choices=NewsType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = 'News'
        verbose_name = 'News'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    theme = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name}'s message"


class SocialMedia(models.Model):
    telegram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    x = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    def __str__(self):
        if self.telegram:
            return {self.telegram}
        return 'Social Media'


class Banner(models.Model):
    image = models.ImageField(upload_to='images/banners/',
                              validators=[FileExtensionValidator(
                                  allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'heif', 'heic', 'avif']),
                                  check_image_size])

    def __str__(self):
        return self.image.url


class About(models.Model):
    happy_clients = models.IntegerField(null=True, blank=True)
    product_type = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Happy clients: {self.happy_clients}+"
