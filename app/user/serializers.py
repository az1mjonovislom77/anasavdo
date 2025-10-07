import re

from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from app.user.models import User, VerificationOTP
from app.user.utils import generate_code
from app.user.validations import check_valid_email, check_valid_phone, validate_phone_number
from app.utils.utility import send_phone_number_code


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'username', 'phone_number',
            'image', 'auth_type', 'password',
            'is_active', 'date_joined'
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }

    def validate(self, data):
        print('data')
        is_active = data.get('is_active')
        username = data.get('username')
        phone_number = data.get('phone_number')

        if is_active is False:
            raise ValidationError({'message': "User not active."})

        if username != phone_number:
            raise ValidationError({'message': "Username and phone number are not matching"})

        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        db_user = User.objects.filter(username=username, is_active=False).first()
        if db_user:
            if db_user.verificationotp_set.filter(expires_time__gte=timezone.now()).exists():
                raise ValidationError("Sizga otp kod yuborilgan")
            else:
                db_user.phone_number = validated_data.get('phone_number')
                db_user.save()

                code = db_user.create_verify_code(User.AuthType.phone_number)
                send_phone_number_code(db_user.phone_number, code)

                return db_user

        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        print('validate_data', validated_data)
        print('user', user)
        if user.auth_type is None:
            user.auth_type = User.AuthType.phone_number
        user.save()

        code = user.create_verify_code(User.AuthType.phone_number)
        send_phone_number_code(user.phone_number, code)

        return user



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'username', 'phone_number',
            'image', 'auth_type', 'password',
            'is_active', 'date_joined'
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "phone_number": {"read_only": True},
        }

    def validate(self, data):
        print(data)
        is_active = data.get('is_active')
        username = data.get('username')
        phone_number = data.get('phone_number')

        if is_active is False:
            raise ValidationError({'message': "User not active."})

        if username != phone_number:
            raise ValidationError({'message': "Username and phone number are not matching"})

        return data


    def update(self, instance, validated_data):
        phone_number = validated_data.get('phone_number')
        username = validated_data.get('username')
        if username != phone_number:
            raise serializers.ValidationError({'message': "You can change your username only by changing your phone number!"})

        validated_data.pop("password", None)
        validated_data.pop("phone_number", None)
        validated_data.pop("username", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=40, required=True)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'password')
        extra_kwargs = {
            "full_name": {"required": True}
        }

    def validate_phone_number(self, phone):
        if phone and not check_valid_phone(phone):
            raise ValidationError("phone number is not valid")

        if User.objects.filter(phone_number=phone, is_active=True).exists():
            raise ValidationError("user with this phone number already exists.")

        return phone

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")

        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("Parolda kamida bitta harf bo‘lishi kerak.")

        if not re.search(r'\d', password):
            raise ValidationError("Parolda kamida bitta raqam bo‘lishi kerak.")

        return password

    def validate(self, data):
        password = data.get('password')
        validate_password(password)

        data['username'] = data.get('phone_number')
        print('data', data)

        return data


    def create(self, validated_data):
        username = validated_data.get('username')
        db_user = User.objects.filter(username=username, is_active=False).first()
        print('db_user', db_user)
        if db_user:
            if db_user.verificationotp_set.filter(expires_time__gte=timezone.now()).exists():
                raise ValidationError("Sizga otp kod yuborilgan")
            else:
                db_user.phone_number = validated_data.get('phone_number')
                db_user.save()

                print('**', User.AuthType.phone_number)

                code = db_user.create_verify_code(User.AuthType.phone_number)
                send_phone_number_code(db_user.phone_number, code)

                return db_user

        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        print('validate_data', validated_data)
        print('user', user)
        # user.is_active = False
        user.save()

        code = user.create_verify_code(User.AuthType.phone_number)
        send_phone_number_code(user.phone_number, code)

        return user


class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise ValidationError("Invalid phone number or password.")

        data['user'] = user
        return data


class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    user = serializers.IntegerField(required=True)

    def validate(self, data):
        code = data.get('code')
        user = data.get('user')
        if len(str(code)) != 6 or not str(code).isdigit():
            raise ValidationError("Invalid data")
        user = User.objects.filter(id=user).first()

        if not user:
            raise ValidationError("Invalid data")

        data['user'] = user
        return data


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "full_name", "phone_number", "image")

        extra_kwargs = {
            "id": {"read_only": True},
            "phone_number": {'read_only': True},
        }

    def validate_full_name(self, value):
        if len(value) <= 3:
            raise ValidationError("Full name must not exceed 3 characters.")
        return value

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['phone_number'] = instance.username
        return data


class ChangePhoneNumberRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, phone_number):
        validate_phone_number(phone_number)
        print('ph', phone_number)
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Phone number already exists.")
        return phone_number


class VerifyPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        code = data.get('code')

        validate_phone_number(phone_number)
        print('useer', self.context['request'].user)

        otp = VerificationOTP.objects.filter(
            user=self.context['request'].user,
            code=code,
            auth_type=VerificationOTP.AuthType.phone_number,
            is_confirmed=False,
            expires_time__gte=timezone.now()
        ).first()

        if not otp:
            raise serializers.ValidationError("Invalid or expired OTP")

        print('otp', otp)

        data['otp_instance'] = otp
        return data


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=40)

    def validate_password(self, password):
        if len(password) <= 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")

        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("Parolda kamida bitta harf bo‘lishi kerak.")

        if not re.search(r'\d', password):
            raise ValidationError("Parolda kamida bitta raqam bo‘lishi kerak.")

        return password


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=40, min_length=4)
    new_password = serializers.CharField(required=True, max_length=40)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if len(new_password) <= 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")

        if not re.search(r'[A-Za-z]', new_password):
            raise ValidationError("Parolda kamida bitta harf bo‘lishi kerak.")

        if not re.search(r'\d', new_password):
            raise ValidationError("Parolda kamida bitta raqam bo‘lishi kerak.")

        if old_password == new_password:
            raise ValidationError("Parollar bir biriga teng bo'la ololmaydi")

        return data
