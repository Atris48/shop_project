# Generated by Django 4.2.6 on 2023-11-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0013_remove_factor_is_create_by_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='unique_id',
            field=models.CharField(max_length=20, null=True, verbose_name='کد پیگیری'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='کد رهگیری'),
        ),
    ]
