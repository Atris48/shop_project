# Generated by Django 4.2.6 on 2023-11-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0022_order_send_sms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factordiscount',
            name='code',
            field=models.CharField(max_length=30, unique=True, verbose_name='کد'),
        ),
    ]
