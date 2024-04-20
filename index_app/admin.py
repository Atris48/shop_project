from django.contrib import admin
from . import models

admin.site.register(models.ReadableArticles)


class SiteVisitAdmin(admin.ModelAdmin):
    list_filter = ['created_at']


admin.site.register(models.SiteVisit, SiteVisitAdmin)
