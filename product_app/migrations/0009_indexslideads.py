# Generated by Django 4.2.6 on 2023-10-31 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0008_product_discounted_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexSlideAds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(upload_to='index/slide_banner')),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]