from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
from account_app.models import User
from ckeditor.fields import RichTextField
from comment.models import Comment


class ArticleCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    site_title_tag = models.CharField(max_length=400, null=True, blank=True, verbose_name='تگ تایتل')
    site_meta_description = models.TextField(null=True, blank=True, verbose_name='متا دسکریپشن')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', null=True, blank=True,
                               verbose_name='زیر مجموعه ی')
    slug = models.SlugField(unique=True, verbose_name='آدرس دسته بندی')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


class Article(models.Model):
    title = models.CharField(max_length=500, verbose_name='عنوان مقاله')
    site_title_tag = models.CharField(max_length=400, null=True, blank=True, verbose_name='تگ تایتل')
    site_meta_description = models.TextField(null=True, blank=True, verbose_name='متا دسکریپشن')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='articles', verbose_name='نویسنده ی مقاله')
    categories = models.ManyToManyField(ArticleCategory, null=True, blank=True, verbose_name='دسته بندی ها')
    visit_count = models.PositiveBigIntegerField(default=0, verbose_name='تعداد بازدید')
    unique_visitors = models.TextField(default="", null=True, blank=True)
    poster = models.ImageField(upload_to='articles/posters', verbose_name='پوستر مقاله')
    short_description = models.TextField(null=True, blank=True, verbose_name='توضیحات کوتاه')
    body = RichTextField(verbose_name='متن مقاله')
    slug = models.SlugField(unique=True, verbose_name='آدرس مقاله', null=True)
    comments = GenericRelation(Comment)
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده؟')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def get_created_at(self):
        date = self.created_at.date()
        persian_months = ['فرودین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                          'اسفند']
        return f'{date.day} / {persian_months[date.month - 1]} / {date.year}'


class BlogAds(models.Model):
    image = models.ImageField(upload_to='blog/ads', verbose_name='تصویر')
    url = models.URLField(null=True, blank=True, verbose_name='لینک تبلیغ')

    class Meta:
        verbose_name = 'عکس تبلیغ بلاگ'
        verbose_name_plural = 'عکس تبلیغ بلاگ ها'

    def __str__(self):
        return f'{self.id}'


class ArticleChoose(models.Model):
    slide_articles = models.ManyToManyField(Article, verbose_name='انتخاب مقالات اسلایدی', null=True, blank=True,
                                            related_name='slides')
    two_articles = models.ManyToManyField(Article, verbose_name='انتخاب دو مقاله', null=True, blank=True,
                                          related_name='two')

    class Meta:
        verbose_name = 'مقاله انتخابی'
        verbose_name_plural = 'مقالات انتخابی'
