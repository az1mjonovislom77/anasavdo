from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from jsonschema.validators import validate
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView

from app.user.models import User, VerificationOTP
from app.user.serializers import (
    SignUpSerializer, SignInSerializer, VerifyOTPSerializer, MeSerializer,
    ChangePasswordSerializer, ResetPasswordSerializer, PhoneNumberSerializer, UserSerializer,
    ChangePhoneNumberRequestSerializer, VerifyPhoneNumberSerializer, CreateUserSerializer
)
from app.user.utils import generate_code
from app.user.validations import IsAdminOrSuperAdmin, validate_phone_number
from app.utils.utility import send_phone_number_code


@extend_schema(tags=["user"])
class UserAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def get(self, request):
        user = User.objects.filter(role=User.UserRole.user, is_active=True)
        serializer = UserSerializer(user, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["user"])
class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_active:
            user.is_active = False
            user.save()
            return Response({'message': "User successfully deleted!"}, status=status.HTTP_200_OK)
        return Response({'message': "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Register'])
class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = SignUpSerializer(data=data)
            if not serializer.is_valid():
                data = {
                    'success': False,
                    'status_code': 400,
                    'errors': serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save(is_active=False)
            data = {
                'success': True,
                'status_code': 200,
                'message': 'OTP code has been sent to phone number',
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            print('errorss', e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Register'])
class SignInView(APIView):
    serializer_class = SignInSerializer

    def post(self, request):
        try:
            serializer = SignInSerializer(data=request.data)
            if not serializer.is_valid():
                data = {
                    'success': False,
                    'status_code': 400,
                    'errors': serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data.get('user')
            data = {
                'success': True,
                'status_code': 200,
                'message': 'user has been logged in successfully',
                'data': user.get_tokens(),
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Admin Login'])
class AdminPanelSignInView(APIView):
    serializer_class = SignInSerializer

    def post(self, request):
        try:
            serializer = SignInSerializer(data=request.data)
            if not serializer.is_valid():
                data = {
                    'success': False,
                    'status_code': 400,
                    'errors': serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data.get('user')

            if user.role == User.UserRole.user:
                return Response({
                    'success': False,
                    'status_code': 400,
                    'message': 'You are not allowed.',
                }, status=status.HTTP_400_BAD_REQUEST)

            print('user', user.role)

            data = {
                'success': True,
                'status_code': 200,
                'message': 'user has been logged in successfully',
                'data': user.get_tokens(),
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'status_code': 400,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            data = {
                'success': False,
                'status_code': 400,
                'errors': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        code = serializer.validated_data.get('code')
        user = serializer.validated_data.get('user')
        otps = user.verificationotp_set.filter(code=code, is_confirmed=False, expires_time__gte=timezone.now()).first()
        if not otps:
            return Response({
                "success": False,
                "status_code": 400,
                "message": "OTP not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        otps.is_confirmed = True
        user.is_active = True
        otps.save()
        user.save()
        return Response({
            "success": True,
            "status_code": 200,
            "data": user.get_tokens()
        })


@extend_schema(tags=['Profile'])
class MeAPIView(RetrieveAPIView):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Profile'])
class MeEditAPIView(UpdateAPIView):
    serializer_class = MeSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put']

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Profile'])
class ChangePhoneNumberRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePhoneNumberRequestSerializer

    def post(self, request):
        serializer = ChangePhoneNumberRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        new_phone_number = serializer.validated_data.get('phone_number')
        user = request.user

        VerificationOTP.objects.filter(user=user, auth_type=VerificationOTP.AuthType.phone_number).delete()

        code = user.create_verify_code(User.AuthType.phone_number)
        send_phone_number_code(new_phone_number, code)
        return Response({
            "success": True,
            "status_code": 200,
            'message': 'OTP code sent to new phone number',
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Profile'])
class VerifyPhoneNumberAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VerifyPhoneNumberSerializer

    def post(self, request):
        serializer = VerifyPhoneNumberSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp_instance']
        phone_number = serializer.validated_data['phone_number']

        user = request.user
        user.phone_number = phone_number
        user.username = phone_number
        user.save()

        otp.is_confirmed = True
        otp.save()

        return Response({
            'success': True,
            'message': "Phone number successfully updated data"
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
class ForgotPasswordAPIView(APIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        try:
            serializer = PhoneNumberSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "status_code": 400,
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            phone_number = serializer.validated_data.get('phone_number')
            user = User.objects.filter(username=phone_number, is_active=True).first()
            if user:
                if user.verificationotp_set.filter(expires_time__gte=timezone.now(), is_confirmed=False).exists():
                    return Response({
                        'success': False,
                        'status_code': 400,
                        'message': 'You have already had a otp code'
                    }, status=status.HTTP_400_BAD_REQUEST)

                VerificationOTP.objects.create(
                    user=user,
                    code=generate_code(),
                    auth_type=VerificationOTP.AuthType.phone_number
                )
                return Response({
                    'success': True,
                    'status_code': 200,
                    'message': 'otp code has been sent your phone_number',
                    'user': user.id
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'success': False,
                    'status_code': 400,
                    'message': 'Phone Number not found'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "status_code": 400,
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            password = serializer.validated_data.get('password')
            user = request.user
            user.set_password(password)
            user.save()
            return Response({
                'success': True,
                'status_code': 200,
                'message': 'Password has been changed successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Profile'])
class DeleteAccountAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = get_object_or_404(User, username=request.user)
        if user.is_active:
            user.is_active = False
            user.save()
            return Response({'message': 'Account has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Account not found'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "status_code": 400,
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            user = request.user
            if not user.check_password(old_password):
                return Response({
                    'success': False,
                    'status_code': 400,
                    'message': 'old password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({
                'success': True,
                'status_code': 200,
                'message': 'The password has been updated successfully'
            })

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
