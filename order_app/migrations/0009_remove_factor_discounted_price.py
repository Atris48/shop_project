# Generated by Django 4.2.6 on 2023-11-08 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0008_alter_factor_discount_alter_factordiscount_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='discounted_price',
        ),
    ]