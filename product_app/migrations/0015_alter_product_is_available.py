# Generated by Django 4.2.6 on 2023-10-31 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0014_product_is_available_alter_product_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='موجود'),
        ),
    ]
