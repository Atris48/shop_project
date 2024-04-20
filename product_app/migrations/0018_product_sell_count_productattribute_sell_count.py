# Generated by Django 4.2.6 on 2023-11-04 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0017_product_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell_count',
            field=models.PositiveIntegerField(default=0, verbose_name='تعداد فروش این محصول'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='sell_count',
            field=models.PositiveIntegerField(default=0, verbose_name='تعداد فروش'),
        ),
    ]