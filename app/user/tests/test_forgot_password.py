import os
os.environ['TESTING'] = '1'

from django.test import TestCase
from django.urls import reverse

from app.user.models import User, VerificationOTP


class ForgotPasswordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="azamat@gmail.com",
            phone_number="+998911111111",
            full_name="azamat berdimurodov"
        )
        self.user.set_password("qwerty1234")
        self.user.save()
        self.user.verificationotp_set.all().delete()

    def test_success_input_email(self):
        response = self.client.post(
            reverse('forgot-password'),
            data={
                'email': 'azamat@gmail.com'
            }
        )
        otps = VerificationOTP.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status_code'], 200)
        self.assertEqual(response.data['user'], self.user.id)

        self.assertEqual(len(otps), 1)
        self.assertEqual(otps.first().user.username, 'azamat@gmail.com')
        self.assertFalse(otps.first().is_confirmed)

        response1 = self.client.post(
            reverse('forgot-password'),
            data={
                'email': 'azamat@gmail.com'
            }
        )
        otps = VerificationOTP.objects.all()
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.data['status_code'], 400)
        self.assertEqual(len(otps), 1)

    def test_wrong_input_email(self):
        response = self.client.post(
            reverse('forgot-password'),
            data={
                'email': 'azam@gmail.com'
            }
        )
        otps = VerificationOTP.objects.all()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status_code'], 400)
        self.assertEqual(len(otps), 0)

    def test_wrong_input_data(self):
        response = self.client.post(
            reverse('forgot-password'),
            data={
                'username': 'azam@gmail.com'
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data['error']['email'][0], 'This field is required.')


class ForgotPasswordVerifyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="azamat@gmail.com",
            phone_number="+998911111111",
            full_name="azamat berdimurodov"
        )
        self.user.set_password("qwerty1234")
        self.user.save()
        self.user.verificationotp_set.all().delete()

        self.client.post(
            reverse('forgot-password'),
            data={
                'email': 'azamat@gmail.com'
            }
        )

    def test_success_verify(self):
        otps = VerificationOTP.objects.first()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'code': otps.code,
                'user': self.user.id
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status_code'], 200)
        self.assertIn('refresh', response.data['data'])
        self.assertIn('access', response.data['data'])

    def test_wrong_credentions(self):
        otp = VerificationOTP.objects.first()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'code': 111111,
                'user': 11
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status_code'], 400)

        response1 = self.client.post(
            reverse('verify-otp'),
            data={
                'code': otp.code,
                'user': 11
            }
        )
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.data['status_code'], 400)

        response2 = self.client.post(
            reverse('verify-otp'),
            data={
                'code': 111111,
                'user': self.user.id
            }
        )
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.data['status_code'], 400)

    def test_other_data(self):
        otp = VerificationOTP.objects.first()
        response = self.client.post(
            reverse('verify-otp'),
            data={
                'just': otp.code,
                'shoot': self.user.id
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.data)
        self.assertEqual(response.data['errors']['code'][0], 'This field is required.')
        self.assertEqual(response.data['errors']['user'][0], 'This field is required.')


class ChangePasswordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="azamat@gmail.com",
            phone_number="+998911111111",
            full_name="azamat berdimurodov"
        )
        self.user.set_password("qwerty1234")
        self.user.save()
        self.user.verificationotp_set.all().delete()

        response = self.client.post(
            reverse('login'),
            data={
                'username': 'azamat@gmail.com',
                'password': 'qwerty1234'
            },
            content_type='application/json'
        )
        self.access = response.data['data']['access']

    def test_success_change_password(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('reset-password'),
            data={
                'password': 'Azamat1234'
            },
            headers=headers
        )
        user = User.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status_code'], 200)
        self.assertTrue(user.check_password('Azamat1234'))

    def test_valid_password(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('reset-password'),
            data={
                'password': 'azamat'
            },
            headers=headers
        )
        user = User.objects.first()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status_code'], 400)
        self.assertFalse(user.check_password('azamat'))

    def test_other_data(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('reset-password'),
            data={
                'just': 'azamat1234'
            },
            headers=headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error']['password'][0], 'This field is required.')

    def test_no_authorizatsion(self):
        response = self.client.post(
            reverse('reset-password'),
            data={
                'just': 'azamat1234'
            }
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
