# Generated by Django 5.1.7 on 2025-03-29 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
