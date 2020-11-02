from django.db import models

# Create your models here.
class Car(models.Model):

    name_ru = models.CharField(max_length=255)

    name_en = models.CharField(max_length=255)

    production_year = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name_ru