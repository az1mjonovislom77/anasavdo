from django.test import TestCase
from django.urls import reverse

from app.user.models import User, VerificationOTP


class RegisterTest(TestCase):
    def test_user_account_is_create(self):
        response = self.client.post(
            reverse('register'),
            data={
                'email': 'azamat@azamat.com',
                'full_name': 'azamat berdimurodov',
                'phone_number': '+998912111111',
                'password': 'azamat1234'
            }
        )

        user = User.objects.get(username='azamat@azamat.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, 'azamat@azamat.com')
        self.assertEqual(user.full_name, 'azamat berdimurodov')
        self.assertEqual(user.phone_number, '+998912111111')
        self.assertTrue(user.check_password('azamat1234'))
        self.assertFalse(user.is_active)

    def test_user_check_password(self):
        response = self.client.post(
            reverse('register'),
            data={
                'email': 'azamat@azamat.com',
                'full_name': 'azamat berdimurodov',
                'phone_number': '+998912111111',
                'password': 'a'
            }
        )

        users = User.objects.all()
        self.assertEqual(len(users), 0)
        self.assertEqual(response.status_code, 400)


class VerifyTest(TestCase):
    def setUp(self):
        self.client.post(
            reverse('register'),
            data={
                'email': 'azamat@azamat.com',
                'full_name': 'azamat berdimurodov',
                'phone_number': '+998912111111',
                'password': 'azamat1234'
            }
        )

    def test_success_verify(self):
        otps = VerificationOTP.objects.all()
        users = User.objects.all()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'code': otps.first().code,
                'user': users.first().id
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.data)
        self.assertIn("refresh", response.data['data'])
        self.assertIn("access", response.data['data'])
        self.assertEqual(len(otps), 1)
        self.assertEqual(len(users), 1)
        self.assertTrue(users.first().is_active)

    def test_failed_verify(self):
        users = User.objects.all()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'code': "111111",
                'user': users.first().id
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(400, response.data['status_code'])
        self.assertEqual("OTP not found", response.data['message'])
        self.assertFalse(users.first().is_active)

    def test_invalid_verify_data(self):
        users = User.objects.all()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'code': "1111111",
                'user': users.first().id
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Invalid data", response.data['errors']['non_field_errors'][0])
        self.assertFalse(users.first().is_active)

    def test_invalid_user_data(self):
        users = User.objects.all()
        otps = VerificationOTP.objects.all()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'code': otps.first().code,
                'user': 11
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Invalid data", response.data['errors']['non_field_errors'][0])
        self.assertFalse(users.first().is_active)
