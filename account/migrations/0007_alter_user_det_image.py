# Generated by Django 4.1.1 on 2022-11-05 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_place_remove_user_det_user_address_user_det_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_det',
            name='image',
            field=models.ImageField(null=True, upload_to='user_pics'),
        ),
    ]
