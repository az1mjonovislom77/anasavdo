from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from app.user.models import User
from app.user.validations import check_image_size
from app.utils.models import Color


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(
        upload_to='images/category/',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp']),
            check_image_size
        ],
        default='images/category/default-category.jpg'
    )
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug or Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            base_slug = slugify(self.name)
            unique_slug = base_slug
            num = 1
            while Category.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    old_price = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/product/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'heic', 'heif']),
        check_image_size])

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} | {self.id}"

    class Meta:
        db_table = 'productimage'
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField(upload_to='images/product/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'heic', 'heif']),
        check_image_size])
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product} | {self.color}, {self.price}"

    class Meta:
        db_table = 'productcolor'
        verbose_name = 'Product color'
        verbose_name_plural = 'Product colors'


class ProductType(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product} | {self.name}"

    class Meta:
        db_table = 'producttype'
        verbose_name = 'Product type'
        verbose_name_plural = 'Product types'


class ProductValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='values')
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    value = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product} | {self.type}, {self.value}"

    class Meta:
        db_table = "productvalue"
        verbose_name = "Product value"
        verbose_name_plural = "Product values"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    message = models.TextField()
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product} | {self.user}"

    class Meta:
        db_table = 'comment'


class CategoryImages(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/category/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'heic', 'heif', 'avif']),
        check_image_size])

    def __str__(self):
        return str(self.category)
