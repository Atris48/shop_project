# Generated by Django 4.2.6 on 2023-10-26 04:06

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=django_jalali.db.models.jDateTimeField(null=True, verbose_name='ناریخ تولد'),
        ),
    ]
