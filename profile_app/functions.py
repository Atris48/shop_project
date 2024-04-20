

def remove_notif(queryset):
    for object in queryset:
        object.remove()
