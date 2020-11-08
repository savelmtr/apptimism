from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import Car

User = get_user_model()


def get_car_from_user(car_pk: int):
    try:
        car = Car.objects.get(pk=car_pk)
        user = car.renter
        car.renter = None
        car.save()

        email_about_taking_car(car, user)
        return 0
    except Exception as e:
        return e


def give_car_to_user(user_pk: int, car_pk: int):
    try:
        user = User.objects.get(pk=user_pk)
        car = Car.objects.get(pk=car_pk)
        car.renter = user
        car.save()

        email_about_giving_car(car, user)
        return 0
    except Exception as e:
        return e


def send_mail_to_user(subject: str, content: str, user: User):
    send_mail(
        subject,
        content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email, ],
    )


def email_about_giving_car(car: Car, user: User):
    content = render_to_string(
        'car_rent/giving_car_email.html', {'car': car, 'user': user})
    subject = _("You've got a new car in rent!")
    return send_mail_to_user(subject, content, user)


def email_about_taking_car(car: Car, user: User):
    content = render_to_string(
        'car_rent/taking_car_email.html', {'car': car, 'user': user})
    subject = _("We stopped leasing a car to you!")
    return send_mail_to_user(subject, content, user)
