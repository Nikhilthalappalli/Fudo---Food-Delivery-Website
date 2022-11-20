# Generated by Django 4.1.1 on 2022-11-11 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0016_offers'),
    ]

    operations = [
        migrations.CreateModel(
            name='restaurant_offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('offer_percentage', models.FloatField()),
                ('offer_max_amount', models.FloatField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurants')),
            ],
        ),
        migrations.DeleteModel(
            name='offers',
        ),
    ]