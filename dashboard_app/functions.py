from datetime import timedelta, datetime

from django.db.models import Count, Sum, F
from django.utils import timezone
from jalali_date import datetime2jalali

from account_app.models import User
from index_app.models import SiteVisit
from order_app.models import Order, OrderItem

current_jalali_date = datetime2jalali(timezone.now())
current_jalali_year = current_jalali_date.year
order_status = ['آماده سازی', 'آماده شده', 'ارسال شده']
today = datetime.today()


def index_order_count_chart(year):
    order_count_data = Order.objects.filter(year=year,
                                            order_status__in=order_status
                                            ).values('month').annotate(
        order_count=Count('id'),
    ).order_by('month')
    order_data_list = list(order_count_data)
    return order_data_list


def index_sell_amount_chart(year):
    sell_data = Order.objects.filter(year=year,
                                     order_status__in=order_status).values(
        'month').annotate(
        sell_mount=Sum('total_price'),
    ).order_by('month')
    sell_data_list = list(sell_data)
    return sell_data_list


def get_site_visits_data_list():
    site_visits_data = SiteVisit.objects.filter(created_at__gte=(today - timedelta(days=365))
                                                ).values('month').annotate(
        visit_count=Count('id'),
    ).order_by('year', 'month')
    site_visits_data_list = list(site_visits_data)
    return site_visits_data_list


def order_chart_data(day, value):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=day)), order_status__in=order_status
                                      ).values(value).annotate(
        order_count=Count('id'),
    ).order_by('year', value)
    order_data_list = list(order_data)
    return order_data_list


def sell_chart_data(day, value):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=day)), order_status__in=order_status
                                      ).values(value).annotate(
        sell_mount=Sum('total_price'),
    ).order_by('year', value)
    order_data_list = list(order_data)
    return order_data_list


def all_order_chart_data():
    order_data = Order.objects.filter(order_status__in=order_status).values('year').annotate(
        order_count=Count('id'),
    ).order_by('year')
    order_data_list = list(order_data)
    return order_data_list


def all_sell_chart_data():
    order_data = Order.objects.filter(order_status__in=order_status).values('year').annotate(
        sell_mount=Sum('total_price'),
    ).order_by('year')
    order_data_list = list(order_data)
    return order_data_list


def product_last_year_order_count(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=365)),
                                      order_status__in=order_status, items__product=product).values('month').annotate(
        order_count=Sum(F('items__quantity')),
    ).order_by('year', 'month')
    order_data_list = list(order_data)
    return order_data_list


def product_last_year_sell_amount(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=365)),
                                      order_status__in=order_status, items__product=product).values('month').annotate(
        order_count=Sum(F('items__price') * F('items__quantity'))
    ).order_by('year', 'month')
    order_data_list = list(order_data)
    return order_data_list


def product_last_month_order_count(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=30)),
                                      order_status__in=order_status, items__product=product).values('day').annotate(
        order_count=Sum(F('items__quantity')),
    ).order_by('day')
    order_data_list = list(order_data)
    return order_data_list


def product_last_month_sell_amount(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=30)),
                                      order_status__in=order_status, items__product=product).values('day').annotate(
        order_count=Sum(F('items__price') * F('items__quantity'))
    ).order_by('day')
    order_data_list = list(order_data)
    return order_data_list


def product_last_week_order_count(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=7)),
                                      order_status__in=order_status, items__product=product).values('day').annotate(
        order_count=Sum(F('items__quantity')),
    ).order_by('day')
    order_data_list = list(order_data)
    return order_data_list


def product_last_week_sell_amount(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=7)),
                                      order_status__in=order_status, items__product=product).values('day').annotate(
        order_count=Sum(F('items__price') * F('items__quantity'))
    ).order_by('day')
    order_data_list = list(order_data)
    return order_data_list


def product_last_day_order_count(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=1)),
                                      order_status__in=order_status, items__product=product).values('hour').annotate(
        order_count=Sum(F('items__quantity')),
    ).order_by('hour')
    order_data_list = list(order_data)
    return order_data_list


def product_last_day_sell_amount(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=1)),
                                      order_status__in=order_status, items__product=product).values('hour').annotate(
        order_count=Sum(F('items__price') * F('items__quantity')),
    ).order_by('hour')
    order_data_list = list(order_data)
    return order_data_list


def product_all_order_count(product):
    order_data = Order.objects.filter(order_status__in=order_status, items__product=product).values('year').annotate(
        order_count=Sum(F('items__quantity')),
    ).order_by('year')
    order_data_list = list(order_data)
    return order_data_list


def product_all_sell_amount(product):
    order_data = Order.objects.filter(order_status__in=order_status, items__product=product).values('year').annotate(
        order_count=Sum(F('items__price') * F('items__quantity')),
    ).order_by('year')
    order_data_list = list(order_data)
    return order_data_list


def product1_comparison_last_year(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=365)),
                                      order_status__in=order_status, items__product__title=product).values(
        'month').annotate(
        sell_amount=Sum(F('items__price') * F('items__quantity')),
    ).order_by('month')
    order_data_list = list(order_data)
    return order_data_list


def product2_comparison_last_year(product):
    order_data = Order.objects.filter(created_at__gte=(today - timedelta(days=365)),
                                      order_status__in=order_status, items__product__title=product).values(
        'month').annotate(
        sell_amount=Sum(F('items__price') * F('items__quantity')),
    ).order_by('month')
    order_data_list = list(order_data)
    return order_data_list


def user_signup_chart(day, value):
    user_data = User.objects.filter(created_at__gte=(today - timedelta(days=day))).values(f'{value}').annotate(
        count=Count('id'),
    ).order_by('year', f'{value}')
    order_data_list = list(user_data)
    return order_data_list
