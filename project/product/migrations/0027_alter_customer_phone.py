# Generated by Django 5.1.4 on 2025-01-08 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
