# Generated by Django 4.2.6 on 2023-12-03 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0009_user_prize_amount_alter_user_day_alter_user_hour_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='prize_amount',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='مقدار جایزه'),
        ),
    ]
