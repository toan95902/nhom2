# Generated by Django 5.1.7 on 2025-03-29 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.IntegerField(default=0),
        ),
    ]
