# Generated by Django 4.2.6 on 2023-11-07 00:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_app', '0025_commentlikedislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='dislikes',
            field=models.ManyToManyField(blank=True, null=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='دیسلایک ها'),
        ),
        migrations.AddField(
            model_name='productcomment',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک ها'),
        ),
        migrations.DeleteModel(
            name='CommentLikeDislike',
        ),
    ]
