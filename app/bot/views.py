import uuid
import threading

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from app.bot.serializers import BotUserSerializer, CodeSerializer
from app.bot.models import BotUser
from app.bot.utils import send_telegram_credentials, create_otp_code, delete_tmp_code
from app.user.authentication import IgnoreBadTokenAuthentication
from app.user.models import User


@extend_schema(tags=['Bot'])
class SaveUserView(generics.CreateAPIView):
    serializer_class = BotUserSerializer
    queryset = BotUser.objects.all()


@extend_schema(tags=['Bot'])
class RegisterVerifyView(APIView):
    serializer_class = CodeSerializer
    authentication_classes = [IgnoreBadTokenAuthentication, ]

    def post(self, request):
        try:
            otp = request.data.get('code')
            if not otp or not str(otp).isdigit() or len(otp) != 6:
                data = {
                    'success': False,
                    'status_code': 400,
                    'message': 'Invalid OTP code'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            botuser = BotUser.objects.filter(tmp_code=otp).first()
            if not botuser:
                data = {
                    'success': False,
                    'status_code': 400,
                    'message': 'OTP not found'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if botuser.user:
                botuser.tmp_code = None
                botuser.save()
                data = {
                    'success': True,
                    'status_code': 200,
                    'data': botuser.user.get_tokens()
                }
                return Response(data, status=status.HTTP_200_OK)

            botuser.tmp_code = None
            username = botuser.username
            if User.objects.filter(username=username).exists():
                print('while ga keldi')
                while True:
                    print('while ga kirdi')
                    username = f"{botuser.username}" + str(uuid.uuid4()).split('-')[-1]
                    if User.objects.filter(username=username).exists():
                        continue
                    else:
                        break

            if User.objects.filter(phone_number=botuser.phone_number).exists():
                user = User.objects.filter(phone_number=botuser.phone_number).first()
                botuser.user = user
                botuser.save()
                data = {
                    'success': True,
                    'status_code': 200,
                    'data': user.get_tokens()
                }
                # data = {
                #     'success': False,
                #     'message': 'phone number already exists'
                # }
                return Response(data, status=status.HTTP_200_OK)

            password = str(uuid.uuid4()).split('-')[0]

            user = User.objects.create(
                username=botuser.username,
                full_name=botuser.full_name,
                phone_number=botuser.phone_number,
                password=password,
                auth_type=User.AuthType.telegram
            )

            user.set_password(user.password)
            user.save()
            botuser.user = user
            botuser.save()
            send_telegram_credentials(botuser.telegram_id, user.phone_number, password)

            data = {
                'success': True,
                'status_code': 200,
                'data': user.get_tokens()
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Bot'])
class RefreshTmpView(APIView):
    serializer_class = None

    def post(self, request):
        try:
            telegram_id = request.data.get('telegram_id')
            if not telegram_id and not str(telegram_id).isdigit():
                data = {
                    'success': False,
                    'status_code': 400,
                    'message': 'Telegram id is not valid'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            botuser = BotUser.objects.filter(telegram_id=telegram_id).first()

            if not botuser:
                data = {
                    'success': False,
                    'message': 'User not found'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if botuser.tmp_code:
                data = {
                    'success': True,
                    'message': 'Your otp code is valid',
                    'otp_valid': True
                }
                return Response(data, status=status.HTTP_200_OK)

            tmp_code = create_otp_code()

            botuser.tmp_code = tmp_code
            botuser.save()
            threading.Timer(60, delete_tmp_code, args=[botuser.id]).start()

            data = {
                'success': True,
                'message': 'otp code has been refreshed',
                'otp_valid': False,
                'otp': str(tmp_code)
            }
            return Response(data)

        except Exception as e:
            data = {
                'success': False,
                'status_code': 400,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
