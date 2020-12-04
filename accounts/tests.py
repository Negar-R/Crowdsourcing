from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from accounts.models import UserProfile
# Create your tests here.


class TestAccountService(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_registeration_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_registeration_POST(self):
        post_data = {
            'username': 'user_test',
            'email': 'user@test.com',
            'password': '1234',
            'user_type': 'contractor'
        }

        response = self.client.post(self.register_url, data=post_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.first().username, 'user_test')
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_POST(self):
        user = User.objects.create(username='second_user_test',
                                   email='second_user@test.com')

        post_data = {
            'email': 'second_user@test.com',
        }

        response = self.client.post(self.login_url, data=post_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(
                         email='second_user@test.com').count(), 1)
        self.assertTemplateUsed(response, 'show_message.html')
