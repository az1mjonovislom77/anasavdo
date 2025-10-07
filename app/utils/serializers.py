from rest_framework import serializers

from app.utils.models import Location, Notification, Currency


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'created')


class CurrencyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name_uz', 'name_en', 'name_ru')
