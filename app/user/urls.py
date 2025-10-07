from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.user.views import (
    SignUpView, SignInView, VerifyOTPView, MeAPIView, MeEditAPIView, ForgotPasswordAPIView,
    ChangePasswordAPIView, DeleteAccountAPIView, ResetPasswordAPIView, AdminPanelSignInView, UserDetailAPIView,
    UserAPIView, VerifyPhoneNumberAPIView, ChangePhoneNumberRequestAPIView
)


urlpatterns = [
    path('', UserAPIView.as_view(), name='user'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('register/', SignUpView.as_view(), name='register'),
    path('verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', SignInView.as_view(), name='login'),

    path('admin/login/', AdminPanelSignInView.as_view(), name='admin-login'),

    path('me/', MeAPIView.as_view(), name='me'),
    path('me-edit/', MeEditAPIView.as_view(), name='me-edit'),
    path('delete-account/', DeleteAccountAPIView.as_view(), name='delete-account'),
    path('change-phone/', ChangePhoneNumberRequestAPIView.as_view(), name='change-number'),
    path('verify-phone/', VerifyPhoneNumberAPIView.as_view(), name='change-number'),

    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ChangePasswordAPIView.as_view(), name='reset-password'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', ResetPasswordAPIView.as_view(), name='change-password'),
]
