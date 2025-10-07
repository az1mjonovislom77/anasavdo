from random import randint
import requests

from django.conf import settings

from app.bot.models import BotUser


def create_otp_code():
    code = ''.join(str(randint(0, 9)) for _ in range(6))

    return code


def delete_tmp_code(user_id):
    user = BotUser.objects.filter(id=user_id).first()
    user.tmp_code = None
    user.save()


def send_telegram_credentials(telegram_id, phone_number, password):
    TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
    message = (
        f"✅ You have successfully registered!\n"
        f"👤 Username: `{phone_number}`\n"
        f"🔐 Password: `{password}`\n\n"
        f"Please keep this information safe."
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=data)
    return response.json()
