# Generated by Django 5.1.4 on 2025-01-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0058_order_created_at_wishlist_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('shipped', 'shipped'), ('Packed', 'Packed'), ('On the way', 'On the way'), ('Deliverd', 'Deliverd'), ('Cancelled', 'Cancelled')], default='Placed', max_length=50),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
