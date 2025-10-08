from urllib.parse import urlparse
import phonenumbers
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError
from app.about.models import OurContact, Contact, SocialMedia, News, \
    Banner, About
from app.user.validations import check_valid_email
from app.utils.utility import ImageOrUrlField
from rest_framework import serializers
from django.conf import settings


class OurContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurContact
        fields = ('id', 'address', 'address_uz', 'address_en', 'address_ru', 'phone_numbers', 'emails', 'working_time',
                  'working_time_uz', 'working_time_en', 'working_time_ru')

    def validate_emails(self, emails):
        print('attrs', emails)
        for email in emails:
            check_valid_email(email)
        return emails

    def validate_phone_numbers(self, phone_numbers):
        print('phone', phone_numbers)
        for phone_number in phone_numbers:
            try:
                parse_number = phonenumbers.parse(phone_number)
                if not phonenumbers.is_valid_number(parse_number):
                    raise ValidationError({
                        'success': False,
                        'message': 'Invalid phone number ⚠️',
                    })
            except phonenumbers.NumberParseException:
                raise ValidationError({
                    'success': False,
                    'message': 'The phone number is in the wrong format! (+_) ⚠️',
                })
        return phone_numbers

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        rep['address'] = getattr(instance, f"address_{lang}", instance.address)
        rep['working_time'] = getattr(instance, f"working_time_{lang}", instance.working_time)
        return rep


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class NewsGetSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(settings.MEDIA_URL + img) for img in obj.images if img]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        rep['title'] = getattr(instance, f"title_{lang}", instance.title)
        rep['description'] = getattr(instance, f"description_{lang}", instance.description)
        return rep


class NewsSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=ImageOrUrlField(),  # Yangi custom field
        write_only=True
    )
    images_urls = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru',
                  'type', 'images', 'images_urls', 'created_at']

    def get_images_urls(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(settings.MEDIA_URL + img) for img in obj.images if img]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        news = News.objects.create(**validated_data)
        paths = []
        for img in images:
            if isinstance(img, str):
                paths.append(img)
            else:
                path = default_storage.save(f"images/news/{img.name}", img)
                paths.append(path)
        news.images = paths
        news.save()
        return news

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if images is not None:

            incoming_paths = []
            for img in images:
                if isinstance(img, str):
                    normalized = self._normalize_path(img)
                    incoming_paths.append(normalized)
                else:
                    incoming_paths.append(img.name)

            for old_image in instance.images[:]:
                if old_image not in incoming_paths:
                    if default_storage.exists(old_image):
                        default_storage.delete(old_image)

            paths = []
            for img in images:
                if isinstance(img, str):
                    normalized = self._normalize_path(img)
                    print('normalized', normalized)
                    paths.append(normalized)
                else:
                    path = default_storage.save(f"images/news/{img.name}", img)
                    print('new path', path)
                    paths.append(path)
            instance.images = paths

        instance.save()
        return instance

    def _normalize_path(self, path_str):
        if path_str.startswith('http'):
            parsed = urlparse(path_str)
            path = parsed.path

            if path.startswith(settings.MEDIA_URL):
                path = path[len(settings.MEDIA_URL):]
            return path
        elif path_str.startswith('images/news/'):
            return path_str
        else:
            return f"images/news/{path_str}"


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Banner
        fields = ('id', 'image')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'
