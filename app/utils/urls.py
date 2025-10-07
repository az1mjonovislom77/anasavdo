from django.urls import path

from app.utils.views import NotificationAPIView, CurrencyGetAPIView, CurrencyAPIView

urlpatterns = [
    path('notification/', NotificationAPIView.as_view(), name='notification'),
    path('currency/', CurrencyGetAPIView.as_view()),
    path('edit-currency/<int:pk>/', CurrencyAPIView.as_view()),
]
