import threading

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.bot.models import BotUser
from app.bot.utils import create_otp_code, delete_tmp_code


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ('telegram_id', 'full_name', 'username', 'phone_number')

    def create(self, validated_data):
        user = BotUser.objects.filter(telegram_id=validated_data.get('telegram_id')).first()
        if not user:
            user = super().create(validated_data)
        user.tmp_code = create_otp_code()
        user.save()
        threading.Timer(60, delete_tmp_code, args=[user.id]).start()

        return user

    def to_representation(self, instance):
        # data = super().to_representation(instance)

        data = {
            "otp": instance.tmp_code
        }
        return data


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
