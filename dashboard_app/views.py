from datetime import datetime, timedelta

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, F, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import Http404

from account_app.models import User, Ban
from chat_app.models import Chat
from index_app.models import SiteVisit
from order_app.models import Order
from . import functions


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                today = datetime.today()
                users = User.objects.filter(is_active=True)
                orders = Order.objects.filter().order_by('-created_at')
                today_orders_count = orders.filter(created_at__date=str(today.date()))
                referral = orders.filter(order_status='مرجوع شده')
                total_sell = orders.filter(order_status__in=functions.order_status).aggregate(Sum('total_price'))
                today_total_sell = orders.filter(order_status__in=functions.order_status,
                                                 created_at__date=str(today.date())).aggregate(Sum('total_price'))
                total_visit = SiteVisit.objects.all()
                today_total_visit = total_visit.filter(created_at__gte=str(today.date()))
                site_visits_data_list = functions.get_site_visits_data_list()
                order_data_list = functions.index_order_count_chart(functions.current_jalali_year)
                sell_data_list = functions.index_sell_amount_chart(functions.current_jalali_year)
                return render(request, 'dashboard_app/index.html',
                              {'visit_count': site_visits_data_list, 'order_data_list': order_data_list,
                               'sell_data_list': sell_data_list, 'orders': orders,
                               'today_orders_count': today_orders_count,
                               'total_visit': total_visit, 'today_total_visit': today_total_visit, 'referral': referral,
                               'total_sell': total_sell, 'users': users, 'today_total_sell': today_total_sell,
                               'year': functions.current_jalali_year})
            else:
                raise Http404()
        else:
            raise Http404()


class ChatListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                chats = Chat.objects.order_by('is_replied')
                page_num = request.GET.get('page', 1)
                paginator = Paginator(chats, 10)
                try:
                    page_obj = paginator.page(page_num)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                return render(request, 'dashboard_app/chat/chat-list.html', {'chats': page_obj})
            else:
                raise Http404()
        else:
            raise Http404()


class MostSellProduct(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                day = request.GET.get('day')
                if day:
                    queryset = Order.objects.filter(
                        created_at__gte=(functions.today - timedelta(days=int(day)))).values(
                        'items__product').annotate(
                        id=F('items__product__id'),
                        order_count=Sum(F('items__quantity')),
                        sell_amount=Sum(F('items__quantity') * F('items__price')),
                        product=F('items__product'),
                        slug=F('items__product__slug'),
                        poster=F('items__product__poster'),
                        title=F('items__product__title'),
                    ).order_by('-order_count')
                    return render(request, 'dashboard_app/orders/order-list.html', {'queryset': queryset})
                else:
                    queryset = Order.objects.all().values(
                        'items__product').annotate(
                        id=F('items__product__id'),
                        order_count=Sum(F('items__quantity')),
                        sell_amount=Sum(F('items__quantity') * F('items__price')),
                        product=F('items__product'),
                        slug=F('items__product__slug'),
                        poster=F('items__product__poster'),
                        title=F('items__product__title'),
                    ).order_by('-order_count')
                    return render(request, 'dashboard_app/orders/order-list.html', {'queryset': queryset})
            else:
                raise Http404()
        else:
            raise Http404()


def admin_ban_user(request, phone):
    if request.user.is_staff:
        user = get_object_or_404(User, phone=phone)
        if Ban.objects.filter(user=user).exists():
            Ban.objects.get(user=user).delete()
            messages.success(request, 'کاربر از مسدودیت خارج شد')
            return redirect('chat_detail', phone)
        else:
            Ban.objects.create(user=user)
            messages.success(request, 'کاربر مسدود شد')
            return redirect('chat_detail', phone)
    else:
        raise Http404()
