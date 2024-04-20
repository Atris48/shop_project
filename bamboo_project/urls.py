"""
URL configuration for bamboo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bamboo_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account_app.urls')),
    path('', include('index_app.urls')),
    path('', include('blog_app.urls')),
    path('', include('product_app.urls')),
    path('', include('about_us_app.urls')),
    path('', include('contact_us_app.urls')),
    path('', include('profile_app.urls')),
    path('', include('order_app.urls')),
    path('', include('dashboard_app.urls')),
    path('', include('chat_app.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('comment/', include('comment.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "ایکات ملی"
admin.site.site_title = "ایکات ملی"
admin.site.index_title = "ایکات ملی"
