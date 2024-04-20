from django.db import models
from django_jalali.db import models as jmodels


class ContactUs(models.Model):
    fullname = models.CharField(max_length=50, verbose_name='نام')
    phone = models.IntegerField(default=0, verbose_name='شماره تلفن')
    email = models.EmailField(verbose_name='ایمیل')
    message = models.TextField(verbose_name='پیام')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما ها'

    def __str__(self):
        return self.fullname
