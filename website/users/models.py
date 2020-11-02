from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


LANGUAGES = [
	('ru', 'Russian'),
	('en', 'English')
]

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    lang = models.CharField("User's language", max_length=2, choices=LANGUAGES, default='ru')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
