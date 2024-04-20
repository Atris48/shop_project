# Generated by Django 4.2.6 on 2023-11-08 02:40

from django.conf import settings
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0026_productcomment_dislikes_productcomment_likes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order_app', '0006_order_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارش ها'},
        ),
        migrations.CreateModel(
            name='FactorDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='کد')),
                ('percentage', models.SmallIntegerField(verbose_name='درصد تخفیف')),
                ('expiration_time', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='زمان انقضا')),
                ('category', models.ManyToManyField(blank=True, null=True, to='product_app.productcategory', verbose_name='برای دسته بندی های')),
                ('products', models.ManyToManyField(blank=True, null=True, to='product_app.product', verbose_name='برای محصولات')),
                ('user', models.ManyToManyField(blank=True, null=True, related_name='factor_discount', to=settings.AUTH_USER_MODEL, verbose_name='برای کاربران')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کد های تخفیف',
            },
        ),
    ]
