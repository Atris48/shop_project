# Generated by Django 4.2.6 on 2023-10-28 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_alter_articlecategory_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='blog/ads', verbose_name='تصویر')),
            ],
        ),
    ]
