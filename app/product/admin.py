from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline as UnfoldTabularInline

from app.product.models import Category, Product, ProductImage, Comment, ProductType, ProductValue, ProductColor, \
    CategoryImages


class ProductImageTabular(UnfoldTabularInline):
    model = ProductImage
    extra = 1


class ProductColorTabular(UnfoldTabularInline):
    model = ProductColor
    extra = 1


class ProductValueTabular(UnfoldTabularInline):
    model = ProductValue
    extra = 1


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, UnfoldModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'is_active')


@admin.register(CategoryImages)
class CategoryImagesAdmin(UnfoldModelAdmin):
    list_display = ('id', 'category', 'image')


@admin.register(ProductType)
class ProductTypeAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ('id', 'product', 'name')


@admin.register(ProductValue)
class ProductValueAdmin(UnfoldModelAdmin):
    list_display = ('id', 'product', 'type', 'value', 'price')


@admin.register(ProductColor)
class ProductColorAdmin(UnfoldModelAdmin):
    list_display = ('id', 'product', 'color', 'price')


@admin.register(Product)
class ProductAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ('title', 'price', 'old_price', 'category', 'is_active')
    inlines = (ProductImageTabular, ProductColorTabular, ProductValueTabular)


@admin.register(ProductImage)
class ProductImageAdmin(UnfoldModelAdmin):
    list_display = ('product', 'image')


@admin.register(Comment)
class CommentAdmin(UnfoldModelAdmin):
    list_display = ('id', 'user', 'product', 'rate', 'is_active')
