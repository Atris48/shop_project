# Generated by Django 4.2.6 on 2023-11-02 07:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_app', '0016_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorites',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_fav', to=settings.AUTH_USER_MODEL, verbose_name='علاقه مندی ها'),
        ),
    ]
