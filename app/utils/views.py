from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from app.user.validations import IsAdminOrSuperAdmin
from app.utils.models import Notification, Currency
from app.utils.serializers import NotificationSerializer, CurrencySerializer, CurrencyGetSerializer


class NotificationAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(Q(user=user) | Q(private=False)).order_by('-created')


class CurrencyGetAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Currency.objects.all()
    serializer_class = CurrencyGetSerializer


class CurrencyAPIView(APIView):
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminOrSuperAdmin,)

    def put(self, request, pk):
        currency = Currency.objects.get(pk=pk)
        serializer = CurrencySerializer(currency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
