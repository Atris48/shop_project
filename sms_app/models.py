from django.db import models
from django_jalali.db import models as jmodels
from account_app.models import User
from order_app.models import FactorDiscount
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


class DiscountSms(models.Model):
    users = models.ManyToManyField(User, verbose_name='انتخاب کاربر ها', null=True, blank=True)
    discount = models.ForeignKey(FactorDiscount, on_delete=models.CASCADE, verbose_name="انتخاب کد تخفیف", blank=True,
                                 null=True)
    is_for_all = models.BooleanField(default=False, verbose_name='ارسال برای همه', null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'اس ام اس تخفیف'
        verbose_name_plural = 'اس ام اس های تخفیف'

    def __str__(self):
        return self.discount.code


@receiver(post_save, sender=DiscountSms)
def product_attribute_create(sender, instance, created, **kwargs):
    if created:
        if instance.is_for_all:
            for user in User.objects.filter(is_admin=False).all():
                print('test', user)


@receiver(m2m_changed, sender=DiscountSms.users.through)
def users_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        if instance.is_for_all and model.objects.filter(pk__in=pk_set).count() != 0:
            instance.delete()
        elif instance.is_for_all == False and model.objects.filter(pk__in=pk_set).count() > 0:
            added_users = model.objects.filter(pk__in=pk_set)
            for user in added_users:
                print('user', user)
