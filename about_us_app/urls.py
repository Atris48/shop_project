from django.urls import path
from . import views

urlpatterns = [
    path('about-us', views.AboutUs.as_view(), name='about_us'),
    path('faq', views.FaqView.as_view(), name='faq'),
]
