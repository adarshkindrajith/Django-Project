# Generated by Django 5.1.4 on 2025-01-22 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0056_remove_order_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='created_at',
        ),
    ]
