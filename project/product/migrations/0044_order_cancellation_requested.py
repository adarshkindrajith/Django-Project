# Generated by Django 5.1.4 on 2025-01-15 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_carouselimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancellation_requested',
            field=models.BooleanField(default=False),
        ),
    ]