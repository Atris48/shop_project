# Generated by Django 4.2.6 on 2023-10-31 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0007_productspecialoffer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discounted_percentage',
            field=models.IntegerField(blank=True, null=True, verbose_name='درصد تخفیف خرده'),
        ),
    ]
