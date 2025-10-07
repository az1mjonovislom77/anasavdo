import secrets

from django.core.mail import send_mail

from core.settings import EMAIL_HOST_USER


def generate_code():
    numbers = '1234567890'
    return ''.join(secrets.choice(numbers) for _ in range(6))


# def send_otp_code_to_email(code, email):
#     message = f"Your OTP code is {code}"
#     send_mail(subject='E-electro', message=message, from_email=EMAIL_HOST_USER, recipient_list=[email])
