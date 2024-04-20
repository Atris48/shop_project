import jdatetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account_app.models import User
from product_app.models import Product, ProductCategory
from django_jalali.db import models as jmodels
from product_app.models import Product
from profile_app.models import Address


class Factor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factors', verbose_name='کاربر')
    total_price = models.PositiveIntegerField(verbose_name='هزینه ی فاکتور', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, verbose_name='آدرس', null=True, blank=True)
    discount = models.ForeignKey('FactorDiscount', on_delete=models.PROTECT, verbose_name='کد تخفیف اعمال شده',
                                 null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتور ها'

    def __str__(self):
        return self.user.phone

    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.price
        return total_price


@receiver(post_save, sender=Factor)
def product_attribute_create(sender, instance, created, **kwargs):
    if created:
        if Factor.objects.filter(user__phone=instance.user.phone).exists():
            factor = Factor.objects.filter(user__phone=instance.user.phone)
            for item in factor[:factor.count() - 1]:
                item.delete()


class FactorItem(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='items', verbose_name='فاکتور')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='factors', verbose_name='محصول')
    size = models.CharField(max_length=10, verbose_name='سایز', null=True, blank=True)
    color = models.CharField(max_length=10, verbose_name='رنگ', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveSmallIntegerField(verbose_name='تعداد')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.product.title

    def get_inventory(self):
        if self.product.inventory:
            return self.product.inventory
        else:
            return self.product.attribute.get(color__fa_title=self.color, size__size_name=self.size).inventory

    def minus_inventory(self, quantity):
        product = self.product
        if product.inventory != None:
            product.inventory -= self.quantity
            product.sell_count += quantity
            if self.product.inventory == 0:
                product.is_available = False
            product.save()
        else:
            object = self.product.attribute.filter(color__fa_title=self.color, size__size_name=self.size).first()
            object.inventory -= self.quantity
            object.sell_count += quantity
            product.sell_count += quantity
            if object.inventory == 0:
                product.is_available = False
                product.save()
            object.save()

    class Meta:
        verbose_name = 'آیتم فاکتور'
        verbose_name_plural = 'آیتم های فاکتور'


class FactorDiscount(models.Model):
    code = models.CharField(max_length=30, verbose_name='کد', unique=True)
    max_price = models.PositiveIntegerField(verbose_name='تا سقف', null=True, blank=True)
    percentage = models.SmallIntegerField(verbose_name='درصد تخفیف')
    user = models.ManyToManyField(User, related_name='factor_discounts', null=True, blank=True,
                                  verbose_name='برای کاربران')
    use = models.ManyToManyField(User, related_name='discount_uses', null=True, blank=True,
                                  verbose_name='استفاده کرده ها')
    products = models.ManyToManyField(Product, null=True, blank=True, verbose_name='برای محصولات')
    category = models.ManyToManyField(ProductCategory, null=True, blank=True, verbose_name='برای دسته بندی های')
    expiration_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='زمان انقضا')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

    def is_valid_for_user(self, user):
        return user in self.user.all()

    def is_valid_for_category(self, categories):
        items = []
        for item in categories:
            if item in self.category.all():
                items.append(True)
            else:
                return item

    def is_valid_for_products(self, product):
        return product in self.products.all()

    def is_expired(self):
        if self.expiration_time:
            now = jdatetime.datetime.now()
            if self.expiration_time < now:
                return True
        return False

    def __str__(self):
        return self.code


class Order(models.Model):
    status_chooses = (
        ("آماده سازی", "آماده سازی"),
        ("آماده شده", "آماده شده"),
        ("ارسال شده", "ارسال شده"),
        ("مرجوع شده", "مرجوع شده"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', verbose_name='کاربر', null=True)
    total_price = models.PositiveIntegerField(verbose_name='هزینه ی سفارش', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, verbose_name='آدرس', null=True, blank=True)
    discount = models.ForeignKey(FactorDiscount, on_delete=models.PROTECT, verbose_name='کد تخفیف اعمال شده',
                                 null=True, blank=True)
    unique_id = models.CharField(max_length=20, verbose_name='کد سفارش', null=True)
    tracking_code = models.CharField(max_length=50, verbose_name='کد رهگیری', null=True, blank=True)
    order_status = models.CharField(choices=status_chooses, default=status_chooses[0], verbose_name='وضعیت سفارش',
                                    max_length=20)
    year = models.IntegerField(default=0, verbose_name='سال', editable=False)
    month = models.IntegerField(default=0, verbose_name='ماه', editable=False)
    day = models.IntegerField(default=0, verbose_name='روز', editable=False)
    hour = models.IntegerField(default=0, verbose_name='ساعت', editable=False)
    send_sms = models.BooleanField(default=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return self.user.phone

    def save(self, *args, **kwargs):
        if self.order_status == 'ارسال شده' and self.send_sms == False:
            # sms
            self.send_sms = True
        super(Order, self).save(*args, **kwargs)

    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.price
        return total_price

    def is_valid_for_referral(self):
        if self.order_status == 'ارسال شده':
            now = jdatetime.datetime.now()
            if (self.updated_at + jdatetime.timedelta(days=1)) > now:
                return True
        return False

    def preparation_percent(self):
        if self.order_status == 'آماده سازی':
            return 30
        elif self.order_status == 'آماده شده':
            return 60
        else:
            return 100

    def preparation_tag(self):
        if self.order_status == 'آماده سازی':
            return 'yellow'
        elif self.order_status == 'آماده شده':
            return 'sky'
        elif self.order_status == 'ارسال شده':
            return 'emerald'
        else:
            return 'zinc'

    def get_created_at(self):
        date = self.created_at.date()
        persian_months = ['فرودین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                          'اسفند']
        return f'{date.day} / {persian_months[date.month - 1]} / {date.year}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name='محصول')
    size = models.CharField(max_length=10, verbose_name='سایز', null=True, blank=True)
    color = models.CharField(max_length=10, verbose_name='رنگ', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveSmallIntegerField(verbose_name='تعداد')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'


class OrderReferral(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='سفارش', related_name='referrals')
    reason = models.TextField(max_length=200, verbose_name='دلیل مرجوع کردن')
    image = models.ImageField(upload_to='order_referral', null=True, blank=True, verbose_name='تصویر مریوطه')

    def __str__(self):
        return self.order.unique_id

    class Meta:
        verbose_name = 'مرجوع'
        verbose_name_plural = 'مرجوعی ها'
