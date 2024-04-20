import jdatetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels

from account_app.models import User


class Notification(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    url = models.URLField(verbose_name='لینک جزییات', null=True, blank=True)
    user = models.ManyToManyField(User, null=True, blank=True, verbose_name='انتخاب کاربران')
    remove_date = jmodels.jDateTimeField(null=True, blank=True, verbose_name='زمان حذف')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلانات'

    def remove(self):
        now = jdatetime.datetime.now()
        if self.remove_date:
            if self.remove_date < now:
                self.delete()
        else:
            if self.created_at + jdatetime.timedelta(days=14) < now:
                self.delete()

    def get_created_at(self):
        date = self.created_at.date()
        persian_months = ['فرودین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                          'اسفند']
        return f'{date.day} / {persian_months[date.month - 1]} / {date.year}'


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    address = models.TextField(verbose_name='نشانی ارسال')
    city = models.CharField(max_length=100, verbose_name='شهر')
    state = models.CharField(max_length=100, verbose_name='استان')
    plaque = models.CharField(max_length=10, verbose_name='پلاک')
    unit = models.CharField(max_length=10, verbose_name='واحد', null=True, blank=True)
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')

    def __str__(self):
        return self.user.phone

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'


class Prize(models.Model):
    amount = models.PositiveIntegerField(verbose_name='مقدار جایزه')
    discount = models.ForeignKey('order_app.FactorDiscount', on_delete=models.CASCADE, verbose_name='کد تخفیف')

    def __str__(self):
        return self.discount.code

    class Meta:
        verbose_name = 'جایزه'
        verbose_name_plural = 'جایزه ها'


@receiver(post_save, sender=Prize)
def product_attribute_create(sender, instance, created, **kwargs):
    if created:
        if instance.discount.user.count() <= 0:
            instance.delete()
