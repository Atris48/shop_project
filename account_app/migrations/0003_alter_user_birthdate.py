# Generated by Django 4.2.6 on 2023-10-26 04:07

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_alter_user_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='ناریخ تولد'),
        ),
    ]