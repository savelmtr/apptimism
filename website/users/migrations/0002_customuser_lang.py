# Generated by Django 3.1.3 on 2020-11-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='lang',
            field=models.CharField(choices=[('ru', 'Russian'), ('en', 'English')], default='ru', max_length=2),
        ),
    ]
