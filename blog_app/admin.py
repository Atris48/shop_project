from django.contrib import admin
from .models import Article, ArticleCategory, BlogAds, ArticleChoose


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'visit_count', 'is_published', 'created_at', 'updated_at']
    list_editable = ['visit_count', 'is_published']
    list_filter = ['is_published', 'categories']
    search_fields = ['title', 'body']


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    list_editable = ['title']
    search_fields = ['title']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleChoose)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(BlogAds)
