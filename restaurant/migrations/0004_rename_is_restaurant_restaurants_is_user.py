# Generated by Django 4.1.1 on 2022-10-18 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_restaurants_is_restaurant_restaurants_user_res_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurants',
            old_name='is_restaurant',
            new_name='is_user',
        ),
    ]
