# Generated by Django 5.1.4 on 2024-12-29 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_brand_product_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]