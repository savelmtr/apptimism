import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

User = get_user_model()


class RegistrationTest(TestCase):

    def setUp(self):
        self.credentials = {
            'email': 'testuser@user.com',
            'first_name': 'Test',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

        self.new_user = {
            'email': 'new@mail.ru',
            'first_name': 'Alex',
            'password1': 'countung4765',
            'password2': 'countung4765',
            'lang': 'en'
        }

    def test_login(self):
        # send login data
        response = self.client.post(
            '/accounts/login/',
            {'username': self.credentials['email'], 'password': self.credentials['password']},
            follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_registration(self):
        self.client.post('/accounts/register/', self.new_user, follow=True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            User.objects.get(email=self.new_user['email']).first_name, self.new_user['first_name'])
        self.assertFalse(User.objects.get(email=self.new_user['email']).is_active)
        assert '/accounts/activate/' in mail.outbox[0].body

    def test_activation(self):
        response = self.client.post('/accounts/register/', self.new_user, follow=True)
        activation_addr = re.search(r'/accounts/activate/.*', mail.outbox[0].body).group(0)
        response = self.client.get(activation_addr, follow=True)
        assert 'Аккаунт успешно активирован' in response.content.decode()
        self.assertTrue(User.objects.get(email=self.new_user['email']).is_active)

    def test_password_change(self):
        new_pass = 'trump2016'
        # логинимся
        self.test_login()
        # меняем пароль
        response = self.client.post(
            '/accounts/password_change/',
            {'old_password': self.credentials['password'],
                'new_password1': new_pass, 'new_password2': new_pass},
            follow=True)

        assert 'Пароль успешно изменен' in response.content.decode()
