from django.db import models
from django_jalali.db import models as jmodels
from blog_app.models import Article


class ReadableArticles(models.Model):
    articles = models.ManyToManyField(Article, verbose_name='مقالات', null=True, blank=True)

    class Meta:
        verbose_name = 'مطلب خواندنی'
        verbose_name_plural = 'مطالب خواندنی'


class SiteVisit(models.Model):
    ip = models.CharField(max_length=200, verbose_name='آی پی', null=True, blank=True)
    os = models.CharField(max_length=50, verbose_name='سیستم عامل', null=True, blank=True)
    browser = models.CharField(max_length=50, verbose_name='مرورگر', null=True, blank=True)
    year = models.IntegerField(default=0, verbose_name='سال', editable=False)
    month = models.IntegerField(default=0, verbose_name='ماه', editable=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'آمار بازدید'
        verbose_name_plural = 'آمار های بازدید'

    def __str__(self):
        return self.ip

    def get_month(self):
        return self.created_at.month
