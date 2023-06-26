# Generated by Django 4.2 on 2023-06-23 09:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_brand_product_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantImage',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='variant_images')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variantimages', to='products.variant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
