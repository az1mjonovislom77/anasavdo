from modeltranslation.translator import register, TranslationOptions

from app.about.models import OurContact, News


@register(OurContact)
class OurContactTranslationOptions(TranslationOptions):
    fields = ('address', 'working_time')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'type', )