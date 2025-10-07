from django.test import TestCase
from django.urls import reverse

from app.user.models import User


class MeUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="azamat",
            phone_number="+998911111111",
            full_name="azamat berdimurodov"
        )
        self.user.set_password("qwerty1234")
        self.user.save()

        response = self.client.post(
            reverse('login'),
            data={
                'username': 'azamat',
                'password': 'qwerty1234'
            }
        )
        self.access = response.data['data']['access']

    def test_success_me(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.get(reverse('me'), headers=headers)
        user = self.user

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.id, response.data['id'])
        self.assertEqual(user.full_name, response.data['full_name'])
        self.assertEqual(user.username, response.data['email'])
        self.assertEqual(user.phone_number, response.data['phone_number'])
        self.assertEqual(user.image, response.data['image'])

    def test_no_token_me(self):
        response = self.client.get(reverse('me'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual("Authentication credentials were not provided.", response.data['detail'])

    def test_edit_success_me(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.put(
            reverse('me-edit'),
            data={
                'full_name': 'azamat bro',
                'phone_number': '+998888888888'
            },
            headers=headers,
            content_type='application/json'
        )
        user = User.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], user.full_name)
        self.assertEqual(response.data['email'], user.username)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['image'], None)
        self.assertEqual(user.phone_number, '+998888888888')
