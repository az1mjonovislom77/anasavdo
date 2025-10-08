from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from app.user.utils import generate_code
from app.user.validations import check_image_size, check_code_validator
from app.user.validations import validate_phone_number
from core.settings import OTP_TIME
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        extra_fields.setdefault("username", phone_number)  # username = phone_number qilib qo'yamiz
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class UserRole(models.TextChoices):
        user = 'u', 'user'
        admin = 'a', 'admin'
        superadmin = 's', 'superadmin'

    class AuthType(models.TextChoices):
        phone_number = 'p', 'phone_number'
        telegram = 't', 'telegram'

    full_name = models.CharField(max_length=70, null=True, blank=True)
    username = models.CharField(max_length=40, unique=True)
    phone_number = models.CharField(max_length=40, unique=True, validators=[validate_phone_number, ])
    image = models.ImageField(upload_to='images/users/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'heic', 'heif', 'avif']),
        check_image_size
    ], null=True, blank=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.user)
    auth_type = models.CharField(max_length=10, choices=AuthType.choices, null=True, blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        db_table = 'user'
        ordering = ['-date_joined']

    def create_verify_code(self, auth_type):
        code = generate_code()
        VerificationOTP.objects.create(
            user=self,
            auth_type=auth_type,
            code=code
        )
        return code

    def __str__(self):
        return str(self.username)


class VerificationOTP(models.Model):
    class AuthType(models.TextChoices):
        phone_number = 'p', 'phone_number'
        telegram = 't', 'telegram'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, validators=[check_code_validator])
    expires_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=10, choices=AuthType.choices, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_time:
            self.expires_time = timezone.now() + timedelta(minutes=OTP_TIME)

        super(VerificationOTP, self).save(*args, **kwargs)

    def __str__(self):
        return f"OTP code for {self.user}"

    class Meta:
        verbose_name = 'Verification OTP'
        verbose_name_plural = 'Verification OTP'
        db_table = 'verifyotp'
