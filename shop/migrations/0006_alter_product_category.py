# Generated by Django 5.1.7 on 2025-03-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20250323_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('electronics', 'Điện - Đồ điện tử'), ('fishing', 'Đồ câu'), ('stationery', 'Đồ dùng học tập'), ('lego', 'Đồ chơi LEGO'), ('furniture', 'Đồ nội thất')], default='electronics', max_length=50),
        ),
    ]
