# Generated by Django 4.2 on 2023-06-30 20:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_rename_quantity_orderitem_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 20, 19, 53, 415911)),
        ),
    ]