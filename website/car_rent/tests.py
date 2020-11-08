from .models import Car
from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model


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
