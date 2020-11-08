import json
from datetime import date

from car_rent.models import Car
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

User = get_user_model()


class APITests(TestCase):

    def setUp(self):
        self.ordinary_user = {
            'email': 'testuser@user.com',
            'first_name': 'Test',
            'password': 'secret',
            'lang': 'en'
        }
        self.super_user = {
            'email': 'admin@user.com',
            'first_name': 'Admin',
            'password': 'foo',
            'lang': 'ru'
        }
        self.user_obj = User.objects.create_user(**self.ordinary_user)
        self.superuser_obj = User.objects.create_superuser(**self.super_user)

        self.car1 = {
            'name_ru': 'Волга',
            'name_en': 'Volga',
            'production_year': 1999
        }

        self.car2 = {
            'name_ru': 'Лада',
            'name_en': 'Lada',
            'production_year': 1985
        }

        self.car1_obj = Car.objects.create(**self.car1)
        self.car2_obj = Car.objects.create(**self.car2)

    def superuser_login(self):
        response = self.client.post(
            '/api/login/',
            {'email': self.super_user['email'], 'password': self.super_user['password']},
            follow=True)
        return json.loads(response.content.decode())['token']

    def test_login(self):
        response = self.client.post(
            '/api/login/',
            {'email': self.ordinary_user['email'], 'password': self.ordinary_user['password']},
            follow=True)
        self.assertTrue('token' in json.loads(response.content.decode()))

    def test_registration(self):
        new_user = {
            'email': 'testing@mail.com',
            'first_name': 'Donald',
            'password': 'unitedwewin',
        }
        self.client.post('/api/register/', new_user, follow=True)

        self.assertTrue(User.objects.filter(email=new_user['email']).exists())

    def test_get_self_cars(self):
        # Дадим пользователю машины
        self.car1_obj.renter = self.user_obj
        self.car1_obj.save()
        self.car2_obj.renter = self.user_obj
        self.car2_obj.save()

        # Залогинимся под пользователем
        response = self.client.post(
            '/api/login/',
            {'email': self.ordinary_user['email'], 'password': self.ordinary_user['password']},
            follow=True)
        token = json.loads(response.content.decode())['token']

        response = self.client.get('/api/cars/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Убедимся, что у нас две машины
        self.assertEqual(len(json.loads(response.content.decode())), 2)

    def test_getting_all_the_users(self):
        # Залогинимся под суперпользователем
        token = self.superuser_login()

        # Получим список всех юзеров
        response = self.client.get('/api/users/', HTTP_AUTHORIZATION=f'Bearer {token}')

        # Убедимся, что у нас всего 2 юзера
        self.assertEqual(len(json.loads(response.content.decode())), 2)

    def test_change_user_data(self):
        # Залогинимся под суперпользователем
        token = self.superuser_login()

        new_data = {
            'email': 'vasya@user.com',
            'first_name': 'Вася',
            'lang': 'en'
        }

        self.client.put(
            f'/api/users/{self.user_obj.pk}', json.dumps(new_data), HTTP_AUTHORIZATION=f'Bearer {token}')

        # Проверим, что данные изменились и старые данные не существуют
        self.assertTrue(User.objects.filter(email=new_data['email']).exists())
        self.assertFalse(User.objects.filter(email=self.ordinary_user['email']).exists())
