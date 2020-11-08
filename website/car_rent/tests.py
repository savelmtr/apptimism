from datetime import date

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from .models import Car

User = get_user_model()


class CarManagersTests(TestCase):

    name_ru = 'Волга'
    name_en = 'Volga'
    production_year = '1999'

    def test_create_car(self):
        car = Car.objects.create(
            name_ru=self.name_ru, name_en=self.name_en, production_year=self.production_year)
        self.assertEqual(car.name_ru, self.name_ru)
        self.assertEqual(car.name_en, self.name_en)
        self.assertEqual(car.production_year, self.production_year)
        self.assertEqual(car.created_at, date.today())

    def test_rent_car_to_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        car = Car.objects.create(
            name_ru=self.name_ru, name_en=self.name_en, production_year=self.production_year)
        car.renter = user
        car.save()

        self.assertEqual(car.renter, user)
        self.assertIn(car, user.car_set.all())


class CarRentTests(TestCase):

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
            '/accounts/login/',
            {'username': self.super_user['email'], 'password': self.super_user['password']},
            follow=True)
        self.assertTrue(response.context['user'].is_superuser)

    def test_carlist(self):
        # логинимся как суперюзер
        self.superuser_login()
        # запрашиваем список всех машин
        response = self.client.get('/car_rent/')

        assert 'Волга' in response.content.decode() and 'Лада' in response.content.decode()

    def test_give_car_to_user(self):
        # логинимся как суперюзер
        self.superuser_login()
        self.client.post(
            f'/car_rent/set_renter/{self.car1_obj.pk}/', {'renter': self.user_obj.pk}, follow=True)
        # проверяем наличие машины среди арендованных у юзера
        self.assertTrue(self.user_obj.car_set.filter(pk=self.car1_obj.pk).exists())
        # проверяем, получил ли арендатор письмо
        self.assertEqual(len(mail.outbox), 1)
        assert "You're receiving this email because since this day we lease you a car" in mail.outbox[0].body

    def test_take_car_from_user(self):
        # логинимся как суперюзер
        self.superuser_login()
        # Дадим пользователю машину
        self.car1_obj.renter = self.user_obj
        self.car1_obj.save()
        self.assertTrue(self.user_obj.car_set.filter(pk=self.car1_obj.pk).exists())

        # а теперь заберём
        self.client.post('/car_rent/', {'car_pk': self.car1_obj.pk}, follow=True)
        self.assertFalse(self.user_obj.car_set.filter(pk=self.car1_obj.pk).exists())

        # проверим почту
        self.assertEqual(len(mail.outbox), 1)
        assert "You're receiving this email because since this day we stop to lease you a car" in mail.outbox[0].body

    def test_create_a_new_car(self):
        # логинимся как суперюзер
        self.superuser_login()

        # Добавляем машину
        new_car = {
            'name_ru': 'Бумер',
            'name_en': 'BMW 7',
            'production_year': 2010
        }

        self.client.post('/car_rent/car/', new_car, follow=True)

        # Проверяем, добавилась ли
        self.assertTrue(Car.objects.filter(name_ru=new_car['name_ru']).exists())
