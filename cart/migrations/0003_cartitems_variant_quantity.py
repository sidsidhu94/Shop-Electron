# Generated by Django 4.2 on 2023-06-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitems_alter_cart_user_delete_cartitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='variant_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
