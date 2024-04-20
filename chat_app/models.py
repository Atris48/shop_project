from django.db import models
from django.db.models import JSONField
from account_app.models import User
from django_jalali.db import models as jmodels


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat', verbose_name='کاربر')
    messages_history = JSONField(default=[], null=True, blank=True, verbose_name='پیام ها')
    is_replied = models.BooleanField(default=False, verbose_name='جواب داده شده؟')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = 'پشتیبانی'
        verbose_name_plural = 'پشتیبانی ها'

    def __str__(self):
        return str(self.user.phone)

    def replied_count(self):
        return Chat.objects.filter(is_replied=True).count()

    def not_replied_count(self):
        return Chat.objects.filter(is_replied=False).count()

    def is_active(self):
        return Chat.objects.filter(is_finished=False).count()
