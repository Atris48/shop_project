# Generated by Django 4.2.6 on 2023-11-11 00:23

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('index_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=200, verbose_name='آی پی')),
                ('os', models.CharField(max_length=50, verbose_name='سیستم عامل')),
                ('browser', models.CharField(max_length=50, verbose_name='مرورگر')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
        ),
    ]
