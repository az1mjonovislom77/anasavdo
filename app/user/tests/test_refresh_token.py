from django.test import TestCase
from django.urls import reverse

from app.user.models import User


class LoginTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='azamat@azamat.com',
            full_name='azamat berdimurodov',
            phone_number='+998912111111'
        )
        user.set_password('azamat1234')
        user.save()
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'azamat@azamat.com',
                'password': 'azamat1234'
            }
        )
        self.refresh = response.data['data']['refresh']

    def test_success_refresh(self):
        response = self.client.post(
            reverse('token-refresh'),
            data={
                'refresh': self.refresh
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_invalid_data(self):
        response = self.client.post(
            reverse('token-refresh'),
            data={
                'refresh': self.refresh + "blablabro"
            }
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Token is invalid')
