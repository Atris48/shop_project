from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from contact_us_app.forms import ContactUsForm
from contact_us_app.rate_limits import contact_rate_limit


class ContactUs(View):
    post_contact_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'contact_us_app/contact_us.html', {'form': form})

    @method_decorator(contact_rate_limit(post_contact_ips, 2, 300))
    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما دریافت شد')
            return redirect('contact_us')
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('contact_us')
