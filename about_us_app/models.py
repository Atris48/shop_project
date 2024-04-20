from django.db import models


class Faq(models.Model):
    question = models.TextField(verbose_name="سوال")
    answer = models.TextField(verbose_name="جواب")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
