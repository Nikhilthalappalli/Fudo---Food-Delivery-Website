# Generated by Django 4.1.1 on 2022-10-22 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_address'),
        ('restaurant', '0007_remove_menu_food_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='food_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.category'),
        ),
    ]
