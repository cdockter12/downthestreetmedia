# Generated by Django 3.0.7 on 2020-07-13 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DTSWebsite', '0002_auto_20200713_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='is_visible',
        ),
    ]
