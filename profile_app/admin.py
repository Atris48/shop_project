from django.contrib import admin
from . import models


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['user', ]
    search_fields = ['title', ]


class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'state', 'plaque', 'unit', 'postal_code']
    list_filter = ['user', ]
    search_fields = ['city', 'state']


admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Prize)
