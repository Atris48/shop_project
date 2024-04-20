from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from about_us_app.models import Faq


class AboutUs(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        return render(request, 'about_us_app/about.html')


class FaqView(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        faqs = Faq.objects.order_by('-id')
        return render(request, 'about_us_app/faq.html', {'faqs': faqs})
