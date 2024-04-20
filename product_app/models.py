from audioop import reverse
from django.contrib.contenttypes.fields import GenericRelation
import jdatetime
from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from comment.models import Comment
from account_app.models import User
from bamboo_project import settings


class ProductCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', null=True, blank=True,
                               verbose_name='زیر مجموعه ی')
    site_title_tag = models.CharField(max_length=400, null=True, blank=True, verbose_name='تگ تایتل')
    site_meta_description = models.TextField(null=True, blank=True, verbose_name='متا دسکریپشن')

    slug = models.SlugField(unique=True, verbose_name='آدرس دسته بندی')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی محصولات'
        verbose_name_plural = 'دسته بندی های محصولات'


class ProductColor(models.Model):
    fa_title = models.CharField(max_length=100, verbose_name='رنگ به فارسی')
    en_title = models.CharField(max_length=100, verbose_name='رنگ به انگلیسی')

    def __str__(self):
        return self.fa_title

    class Meta:
        verbose_name = 'رنگ محصولات'
        verbose_name_plural = 'رنگ های محصولات'


class ProductSize(models.Model):
    size_name = models.CharField(max_length=100, verbose_name='سایز')

    def __str__(self):
        return self.size_name

    class Meta:
        verbose_name = 'سایز محصولات'
        verbose_name_plural = 'سایز های محصولات'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/images')

    class Meta:
        verbose_name = 'عکس محصولات'
        verbose_name_plural = 'عکس های محصولات'

    def __str__(self):
        return self.image.name


class ProductProperty(models.Model):
    value = models.CharField(max_length=255, verbose_name='ویژگی')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'ویژگی محصولات'
        verbose_name_plural = 'ویژگی های محصولات'


class Product(models.Model):
    title = models.CharField(max_length=500, verbose_name='عنوان محصول')
    site_title = models.CharField(max_length=400, null=True, blank=True, verbose_name='عنوان صفحه')
    site_meta_description = models.TextField(null=True, blank=True, verbose_name='متا دسکریپشن')
    description = RichTextField(null=True, blank=True, verbose_name='توضحات محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت محصول')
    discounted_percentage = models.IntegerField(null=True, blank=True, verbose_name='درصد تخفیف خرده')
    discounted_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت تخفیف خورده')
    inventory = models.IntegerField(null=True, blank=True, verbose_name='موجودی')
    category = models.ManyToManyField(ProductCategory, null=True, blank=True, verbose_name='دسته بندی')
    attribute = models.ManyToManyField('ProductAttribute', null=True, blank=True, related_name='products',
                                       verbose_name='سایز بندی و رنگ بندی')
    favorites = models.ManyToManyField(User, null=True, blank=True, verbose_name='علاقه مندی ها',
                                       related_name='product_fav')
    specifications = models.JSONField(null=True, blank=True, verbose_name='مشخصات محصول')
    property = models.ManyToManyField(ProductProperty, null=True, blank=True, verbose_name='ویژگی ها')
    poster = models.ImageField(upload_to='products/posters', null=True, blank=True, verbose_name='پوستر محصول')
    image = models.ManyToManyField(ProductImage, null=True, blank=True, verbose_name='تصاویر محصول')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    is_available = models.BooleanField(default=True, verbose_name='موجود')
    slug = models.SlugField(allow_unicode=True, verbose_name='آدرس محصول')
    sell_count = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش این محصول')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        ordering = ['-is_available', '-created_at']
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.slug)])

    def product_is_available(self):
        if self.inventory:
            if self.inventory != 0:
                return True
        elif self.attribute.all():
            for object in self.attribute.all():
                if object.inventory != 0:
                    return True
        return False

    def has_attribute(self):
        if self.attribute.count() > 0:
            return True
        return False

    def get_share_link(self):
        domain = settings.ALLOWED_HOSTS[0]
        return f'{domain}:8000/product-detail/{self.slug}'

    def get_rate(self):
        comments = self.productcomment_set
        return int((comments.filter(opinion='پیشنهاد میکنم', is_publish=True).count() / comments.count()) * 100)

    def check_user_buy_product(self, user):
        orders = user.orders.all()
        for order in orders:
            for item in order.items.all():
                if self == item.product:
                    return True
        return False

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes', null=True, blank=True,
                                verbose_name='محصول')
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT, null=True, blank=True, verbose_name='رنگ')
    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, null=True, blank=True, verbose_name='سایزم')
    sell_count = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')
    inventory = models.SmallIntegerField(verbose_name='موجودی')

    class Meta:
        verbose_name = 'خصوصیت محصول'
        verbose_name_plural = 'خصوصیات محصول'

    def __str__(self):
        return f'{self.product.title[:30]} - {self.size} - {self.color} - {self.inventory}'


@receiver(post_save, sender=ProductAttribute)
def product_attribute_create(sender, instance, created, **kwargs):
    if created:
        if ProductAttribute.objects.filter(product=instance.product, color=instance.color, size=instance.size).exists():
            attribute = ProductAttribute.objects.filter(product=instance.product, color=instance.color,
                                                        size=instance.size)
            for item in attribute[:attribute.count() - 1]:
                item.delete()


class ProductSpecialOffer(models.Model):
    products = models.ManyToManyField(Product, null=True, blank=True, verbose_name='محصولات')

    class Meta:
        verbose_name = 'پیشنهاد ویژه'
        verbose_name_plural = 'پیشنهادات ویژه'


class IndexSlideAds(models.Model):
    banner = models.ImageField(upload_to='index/slide_banner', verbose_name='تصویر')
    url = models.URLField(null=True, blank=True, verbose_name='آدرس')

    def __str__(self):
        return self.banner.name

    class Meta:
        verbose_name = 'بنر اسلایدی صفحه اصلی'
        verbose_name_plural = 'بنر های اسلایدی صفحه اصلی'


class IndexMobileBoxAds(models.Model):
    banner = models.ImageField(upload_to='index/slide_banner', verbose_name='تصویر')
    url = models.URLField(null=True, blank=True, verbose_name='آدرس')

    def __str__(self):
        return self.banner.name

    class Meta:
        verbose_name = 'بنر باکسی موبایل'
        verbose_name_plural = 'بنر های باکسی موبایل'


class IndexDesktopBoxAds(models.Model):
    banner = models.ImageField(upload_to='index/slide_banner', verbose_name='تصویر')
    url = models.URLField(null=True, blank=True, verbose_name='آدرس')

    def __str__(self):
        return self.banner.name

    class Meta:
        verbose_name = 'بنر باکسی دسکتاپ'
        verbose_name_plural = 'بنر های باکسی دسکتاپ'


class ChosenProduct(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان لیست')
    products = models.ManyToManyField(Product, verbose_name='انتخاب محصولات')
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لیست محصولات'
        verbose_name_plural = 'لیست های محصولات'


class ProductComment(models.Model):
    opinion_chose = (
        ('پیشنهاد میکنم', 'پیشنهاد میکنم'),
        ('پیشنهاد نمیکنم', 'پیشنهاد نمیکنم'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    title = models.CharField(max_length=100, verbose_name='عنوان دیدگاه')
    opinion = models.CharField(choices=opinion_chose, verbose_name='نوع پیشنهاد', max_length=20)
    text = models.TextField(verbose_name='متن دیدگاه')
    is_publish = models.BooleanField(default=False, verbose_name='منتشر شود؟')
    likes = models.ManyToManyField(User, verbose_name='لایک ها', null=True, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, verbose_name='دیسلایک ها', null=True, blank=True,
                                      related_name='comment_dislikes')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.product.title

    def get_created_at(self):
        date = self.created_at.date()
        persian_months = ['فرودین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                          'اسفند']
        return f'{date.day} / {persian_months[date.month - 1]} / {date.year}'

    class Meta:
        verbose_name = 'دیدگاه محصول'
        verbose_name_plural = 'دیدگاه های محصول'
