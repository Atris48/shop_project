from django.contrib import admin
from .models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_replied', 'created_at', 'updated_at']
    list_filter = ['created_at']
    list_editable = ['is_replied']
    search_fields = ['user']


admin.site.register(Chat, ChatAdmin)
