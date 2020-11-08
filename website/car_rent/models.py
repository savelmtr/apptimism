from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Car(models.Model):

    name_ru = models.CharField(max_length=255)

    name_en = models.CharField(max_length=255)

    production_year = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)

    renter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_ru
