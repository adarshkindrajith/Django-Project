# Generated by Django 5.1.4 on 2025-01-22 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0048_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(blank=True, null=True),
        ),
    ]
