# Generated by Django 4.2.6 on 2023-11-11 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0005_sitevisit_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitevisit',
            name='month',
            field=models.IntegerField(default=0, verbose_name='ماه'),
        ),
        migrations.AlterField(
            model_name='sitevisit',
            name='year',
            field=models.IntegerField(default=0, verbose_name='سال'),
        ),
    ]
