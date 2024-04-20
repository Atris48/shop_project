# Generated by Django 4.2.6 on 2023-12-03 17:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order_app', '0025_alter_order_day_alter_order_hour_alter_order_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='factordiscount',
            name='use',
            field=models.ManyToManyField(blank=True, null=True, related_name='discount_uses', to=settings.AUTH_USER_MODEL, verbose_name='استفاده کرده ها'),
        ),
    ]