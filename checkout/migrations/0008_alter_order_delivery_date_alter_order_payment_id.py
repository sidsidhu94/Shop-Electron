# Generated by Django 4.2.2 on 2023-07-01 05:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 8, 5, 36, 48, 74560)),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_id',
            field=models.CharField(max_length=250, null=True),
        ),
    ]