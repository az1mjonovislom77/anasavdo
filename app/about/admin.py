from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline as UnfoldTabularInline

from app.about.models import OurContact, News, Contact, SocialMedia, Banner, About



@admin.register(OurContact)
class OurContactAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ('short_address', 'phone_numbers', 'emails', 'short_work_time')

    def short_work_time(self, obj):
        return f"{obj.working_time[:25]}..."

    def short_address(self, obj):
        return f"{obj.address[:25]}..."

    short_address.admin_order_field = 'address'
    short_work_time.admin_order_field = 'working_time'



@admin.register(News)
class NewsAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ('id', 'title', 'short_description', 'type', 'images', 'created_at')
    # inlines = [NewsImagesInline]

    def short_description(self, obj):
        return f"{obj.description[:25]}..."
    short_description.admin_order_field = 'description'


@admin.register(Contact)
class ContactAdmin(UnfoldModelAdmin):
    list_display = ('id', 'first_name', 'email', 'short_theme')

    def short_theme(self, obj):
        return f"{obj.theme[:25]}..."
    short_theme.admin_order_field = 'theme'


@admin.register(SocialMedia)
class SocialMediaAdmin(UnfoldModelAdmin):
    list_display = ('telegram', 'instagram', 'facebook', 'youtube')


@admin.register(Banner)
class BannerAdmin(UnfoldModelAdmin):
    list_display = ('id', 'image')


@admin.register(About)
class AboutAdmin(UnfoldModelAdmin):
    list_display = ('happy_clients', 'product_type', 'experience')