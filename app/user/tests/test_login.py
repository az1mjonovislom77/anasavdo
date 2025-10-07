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

    def test_success_login(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'azamat@azamat.com',
                'password': 'azamat1234'
            }
        )
        users = User.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 1)
        self.assertIn('data', response.data)
        self.assertIn('refresh', response.data['data'])
        self.assertIn('access', response.data['data'])

    def test_failed_login_with_password(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'azamat@azamat.com',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertNotIn('data', response.data)

    def test_failed_login_with_username(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'wrong@azamat.com',
                'password': 'azamat1234'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertNotIn('data', response.data)

    def test_required_fields(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'azamat@azamat.com'
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data['errors'])
        self.assertEqual('This field is required.', response.data['errors']['password'][0])

        response = self.client.post(
            reverse('login'),
            data={
                'password': 'password'
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data['errors'])
        self.assertEqual('This field is required.', response.data['errors']['username'][0])