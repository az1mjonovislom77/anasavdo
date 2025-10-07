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
        self.access = response.data['data']['access']

    def test_success_reset_password(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('change-password'),
            data={
                'old_password': 'azamat1234',
                'new_password': '1234azamat'
            },
            headers=headers
        )
        user = User.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.check_password('1234azamat'))
        self.assertFalse(user.check_password('azamat1234'))

    def test_wrong_old_password(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('change-password'),
            data={
                'old_password': 'azamat12345',
                'new_password': '1234azamat'
            },
            headers=headers
        )
        user = User.objects.first()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(user.check_password('1234azamat'))

    def test_equal_password(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('change-password'),
            data={
                'old_password': 'azamat1234',
                'new_password': 'azamat1234'
            },
            headers=headers
        )
        user = User.objects.first()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status_code'], 400)

    def test_novalidate_password(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.post(
            reverse('change-password'),
            data={
                'old_password': 'azamat1234',
                'new_password': 'azamat'
            },
            headers=headers
        )
        user = User.objects.first()
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data['error'])

