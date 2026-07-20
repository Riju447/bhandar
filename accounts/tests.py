from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignUpViewTests(TestCase):

    def test_signup_creates_active_user(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'Testpass123!',
                'password2': 'Testpass123!',
            },
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_active)

    def test_signup_accepts_a_more_natural_username(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'Normal User',
                'email': 'normaluser@example.com',
                'password1': 'Testpass123!',
                'password2': 'Testpass123!',
            },
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='Normal User')
        self.assertTrue(user.is_active)

    def test_user_can_login_after_signup(self):
        self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password1': 'Testpass123!',
                'password2': 'Testpass123!',
            },
        )

        login_response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'testuser',
                'password': 'Testpass123!',
            },
            follow=True,
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)