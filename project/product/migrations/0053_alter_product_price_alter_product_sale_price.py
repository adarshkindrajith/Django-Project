# Generated by Django 5.1.4 on 2025-01-22 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0052_alter_product_price_alter_product_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
