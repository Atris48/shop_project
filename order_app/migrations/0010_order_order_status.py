# Generated by Django 4.2.6 on 2023-11-09 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0009_remove_factor_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('آماده سازی', 'آماده سازی'), ('آماده شده', 'آماده شده'), ('ارسال شده', 'ارسال شده'), ('مرجوع شده', 'مرجوع شده')], default=('آماده سازی', 'آماده سازی'), max_length=20, verbose_name='وضعیت سفارش'),
        ),
    ]
