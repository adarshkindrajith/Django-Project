# Generated by Django 5.1.4 on 2024-12-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_is_sale_product_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
