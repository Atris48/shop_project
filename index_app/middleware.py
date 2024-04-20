import jdatetime
from django.shortcuts import render

from bamboo_project import settings
from index_app.models import SiteVisit


class VisitCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = jdatetime.datetime.now()
        info = request.user_agent
        os = info.os.family
        browser = info.browser.family
        ip_address = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
        if not SiteVisit.objects.filter(os=os, browser=browser, ip=ip_address).exists():
            SiteVisit.objects.create(os=os, browser=browser, ip=ip_address, year=now.year, month=now.month)
        else:
            instance = SiteVisit.objects.get(os=os, browser=browser, ip=ip_address)
            if (instance.created_at + jdatetime.timedelta(days=30)) < now:
                instance.ip = None
                instance.save()
        response = self.get_response(request)
        return response


class UnderMaintenance:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.UNDER_MAINTENANCE:
            return render(request, 'maintenance.html')
        response = self.get_response(request)
        return response
