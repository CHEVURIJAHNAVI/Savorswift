# Generated by Django 5.0.7 on 2024-12-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0003_remove_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
