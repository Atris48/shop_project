# Generated by Django 4.2.6 on 2023-11-11 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0002_sitevisit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitevisit',
            name='browser',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='مرورگر'),
        ),
        migrations.AlterField(
            model_name='sitevisit',
            name='ip',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='آی پی'),
        ),
        migrations.AlterField(
            model_name='sitevisit',
            name='os',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='سیستم عامل'),
        ),
    ]
