from django.test import TestCase
from django.urls import reverse

from app.user.models import User


class DeleteAccountTest(TestCase):
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

    def test_success_delete(self):
        headers = {
            'AUTHORIZATION': f'Bearer {self.access}'
        }
        response = self.client.delete(
            reverse('delete-account'), headers=headers
        )

        self.assertEqual(response.status_code, 204)
