from django.test import TestCase
from django.urls import reverse

from app.bot.models import BotUser


class UserSaveTest(TestCase):
    def test_create_success_user(self):
        response = self.client.post(
            reverse('save_user'),
            data={
                "telegram_id": "1028459910",
                "full_name": "abduqodir dusmurodov",
                "username": "atur12a",
                "phone_number": "+9989122101437"
            }
        )

        botuser = BotUser.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertIn('otp', response.data)
        self.assertEqual(len(botuser), 1)
        self.assertEqual(botuser[0].user, None)


class TestUserTest(TestCase):
    def setUp(self):
        self.db_user = self.client.post(
            reverse('save_user'),
            data={
                "telegram_id": "1028459910",
                "full_name": "abduqodir dusmurodov",
                "username": "atur12a",
                "phone_number": "+9989122101437"
            }
        )

    def test_again_user(self):
        response = self.client.post(
            reverse('save_user'),
            data={
                "telegram_id": "1028459910",
                "full_name": "abduqodir dusmurodov",
                "username": "atur12a",
                "phone_number": "+9989122101437"
            }
        )

        users = BotUser.objects.all()
        self.assertEqual(response.status_code, 400)
        self.assertEqual("bot user with this telegram id already exists.", response.data['telegram_id'][0])
        self.assertEqual(len(users), 1)

    # def test_verify_code(self):
    #     code = self.db_user.data['otp']
    #
