from modeltranslation.translator import register, TranslationOptions
from app.product.models import Category, Product, ProductType


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(ProductType)
class ProductTypeTranslation(TranslationOptions):
    fields = ('name',)
