from modeltranslation.translator import register, TranslationOptions

from app.utils.models import Color, Currency


@register(Color)
class ColorTranslation(TranslationOptions):
    fields = ('name', )


@register(Currency)
class CurrencyTranslation(TranslationOptions):
    fields = ('name', )