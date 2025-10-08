import phonenumbers
from django.core.exceptions import ValidationError
import re
from rest_framework import permissions


def check_image_size(image):
    if image.size > 4 * 1024 * 1024:
        raise ValidationError("The image is too long")


def check_code_validator(obj):
    if not str(obj).isdigit() or len(str(obj)) != 6:
        raise ValidationError(message="OTP code is invalid")


def check_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email):
        return False
    return True


def check_valid_phone(phone):
    if phone[0] == '+' and str(phone[1:]).isdigit() and len(phone) > 10:
        return True
    return False


def validate_phone_number(value):
    try:
        parsed_number = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(parsed_number) or not str(value[1:]).isdigit():
            raise ValidationError(message="Your phone number is in the wrong format")

        return True
    except phonenumbers.NumberParseException:
        raise ValidationError(message="Your phone number is in the wrong format. (+_)")


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        from app.user.models import User
        return bool(request.user.is_authenticated and
                    (request.user.role == User.UserRole.admin or request.user.role == User.UserRole.superadmin))


class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        print('salom1')
        print('obj')
        from app.user.models import User
        if request.user.role == User.UserRole.admin or request.user.role == User.UserRole.superadmin:
            print('salom2')
            return True
        return True
