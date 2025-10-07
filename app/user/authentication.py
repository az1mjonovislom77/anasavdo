from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser


class IgnoreBadTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')

        # Agar token yo'q bo'lsa — shunchaki anonim foydalanuvchi sifatida o'tkazamiz
        if not auth:
            return (AnonymousUser(), None)

        try:
            # Bu yerda siz haqiqiy token tekshiruvini qilishingiz mumkin,
            # lekin xatolik bo'lsa ham return AnonymousUser()
            # Masalan, noto'g'ri token bo'lsa ham Exception chiqarmaymiz
            token = auth.replace("Bearer ", "")
            user = ...  # token asosida foydalanuvchini aniqlang (yoki bo‘sh qoldiring)
            return (user, None)
        except Exception:
            # Token yaroqsiz — AnonymousUser qaytaramiz
            return (AnonymousUser(), None)
