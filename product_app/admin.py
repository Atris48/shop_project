from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'price', 'inventory', 'is_published', 'created_at', 'updated_at']
    list_editable = ['price', 'is_published']
    list_filter = ['is_published', 'category']
    search_fields = ['title']


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'inventory', 'sell_count']
    list_filter = ['product', 'sell_count']
    search_fields = ['product']


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', ]
    search_fields = ['title', ]


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'title', 'opinion', 'created_at']
    search_fields = ['title', 'user']
    list_filter = ['user', 'product', 'is_publish']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductColor)
admin.site.register(models.ProductSize)
admin.site.register(models.ProductAttribute, ProductAttributeAdmin)
admin.site.register(models.ProductProperty)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductSpecialOffer)
admin.site.register(models.IndexSlideAds)
admin.site.register(models.IndexDesktopBoxAds)
admin.site.register(models.IndexMobileBoxAds)
admin.site.register(models.ChosenProduct)
admin.site.register(models.ProductComment, ProductCommentAdmin)
