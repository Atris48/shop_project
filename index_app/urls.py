from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('return-terms', views.return_terms,  name='return_terms'),
    path('terms-and-rules', views.terms_and_rules,  name='terms_and_rules'),
]
