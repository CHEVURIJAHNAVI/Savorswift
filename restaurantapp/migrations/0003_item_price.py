# Generated by Django 5.0.7 on 2024-12-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapp', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.BigIntegerField(default=0),
        ),
    ]
