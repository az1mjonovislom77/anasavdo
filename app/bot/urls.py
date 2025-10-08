from django.urls import path

from app.bot.views import SaveUserView, RegisterVerifyView, RefreshTmpView

urlpatterns = [
    path('save_user/', SaveUserView.as_view(), name='save_user'),
    path('register-verify/', RegisterVerifyView.as_view(), name='register-verify'),
    path('refresh-tmpcode/', RefreshTmpView.as_view(), name='refresh-tmpcode'),
]
