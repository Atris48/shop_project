# Generated by Django 4.2.6 on 2023-11-03 04:07

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0002_notification_remove_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='remove_date',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='زمان حذف'),
        ),
    ]
