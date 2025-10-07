import threading
import requests
from core.settings import BASE_URL, BEARER



# # # OTP part ended --------------------------------------------------------------------------------------->

token = BEARER
base_url = BASE_URL


# class PhoneThread(threading.Thread):
#     def __init__(self, message):
#         self.message = message
#         threading.Thread.__init__(self)
#
#     def run(self):
#         print('run func: ', self.message)
#
#
# class PhoneSender:
#     @staticmethod
#     def send_code(data):
#         message = f"To: {data['to_phone']}\nCode: {data['body']}"
#         PhoneThread(message).start()

#
# def send_phone_code(phone_number, code):
#     message_body = (f"--------------------------------------------------------------\n"
#                     f"|            Sizning tasdiqlash kodingiz: >>> {code} <<<             |\n"
#                     f"--------------------------------------------------------------------\n")
#     PhoneSender.send_code(
#         {
#             'to_phone': phone_number,
#             'body': message_body,
#         }
#     )

def send_phone_number_code(phone, code):
    print(f"""   ----------------------------------------
   |          phone: {phone}        |
   |          code: {code}                |
    ---------------------------------------""")
    pass
#     message = f"Bu Eskiz dan test"
#     url = base_url
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     data = {
#         "mobile_phone": phone,
#         "message": message
#     }
#     requests.post(url, headers=headers, data=data)



# # # OTP part ended --------------------------------------------------------------------------------------->


from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile  # Fayl turini tekshirish uchun


class ImageOrUrlField(serializers.ImageField):
    def to_internal_value(self, data):
        # Agar data allaqachon string (URL) bo'lsa, uni shunchaki qaytar — validation qilma
        if isinstance(data, str):
            return data

        # Aks holda, standart ImageField validationini ishlat (fayl bo'lsa)
        return super().to_internal_value(data)
