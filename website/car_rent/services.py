from django.contrib.auth import get_user_model
from .models import Car
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()


def get_car_from_user(car):
    try:
        car.renter = None
        car.save()
        return True
    except Exception as e:
        print(e)
        return False


def give_car_to_user(user_pk:int, car_pk:int):
    try:
        user = User.objects.get(pk=user_pk)
        car = Car.objects.get(pk=car_pk)
        car.renter = user
        car.save()
        return True
    except Exception as e:
        print(e)
        return False

def send_mail_to_user(subject, content, user):
    send_mail(
        subject,
        content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

def email_about_giving_car(car, user):
    content = render_to_string(
        'car_rent/giving_car_email.html', {'car': car, 'user': user})
    subject = _() # Доделать