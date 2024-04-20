# Generated by Django 4.2.6 on 2023-10-26 03:54

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='تلفن همراه')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('fullname', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('national_code', models.CharField(max_length=11, verbose_name='کد ملی')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user/avatars', verbose_name='تصویر پروفایل')),
                ('birthdate', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='ناریخ تولد')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان عضویت')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت کاربر')),
                ('is_admin', models.BooleanField(default=False, verbose_name='ادمین')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربرها',
            },
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11, verbose_name='تلفن همراه')),
                ('code', models.SmallIntegerField(verbose_name='کد اعتبار سنجی')),
                ('expiration_date', django_jalali.db.models.jDateTimeField(verbose_name='تاریخ انقضا')),
            ],
            options={
                'verbose_name': 'اعتبار سنجی',
                'verbose_name_plural': 'اعتبار سنجی ها',
            },
        ),
    ]
