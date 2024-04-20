import random
from datetime import timedelta

from account_app.models import User
from .functions import today
from django.db.models import Sum, F, Count
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404

from order_app.models import OrderItem, Order
from product_app.models import Product
from . import functions


class LastMonthOrderChart(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                last_month_order_data = functions.order_chart_data(30, 'day')
                last_month_sell_data = functions.sell_chart_data(30, 'day')
                label = 'ماه گذشته'
                return render(request, 'dashboard_app/charts/order_sell_chart.html',
                              {'label': label, 'order_data': last_month_order_data, 'sell_data': last_month_sell_data})
            else:
                raise Http404()
        else:
            raise Http404()


class LastWeekOrderChart(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                last_week_order_data = functions.order_chart_data(7, 'day')
                last_week_sell_data = functions.sell_chart_data(7, 'day')
                label = 'هفته گذشته'
                return render(request, 'dashboard_app/charts/order_sell_chart.html',
                              {'label': label, 'order_data': last_week_order_data, 'sell_data': last_week_sell_data})
            else:
                raise Http404()
        else:
            raise Http404()


class LastDayOrderChart(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                last_day_order_data = functions.order_chart_data(1, 'hour')
                last_day_sell_data = functions.sell_chart_data(1, 'hour')
                label = 'روز گذشته'
                return render(request, 'dashboard_app/charts/order_sell_chart.html',
                              {'label': label, 'order_data': last_day_order_data, 'sell_data': last_day_sell_data})
            else:
                raise Http404()
        else:
            raise Http404()


class LastYearOrderChart(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                last_year_order_data = functions.order_chart_data(365, 'month')
                last_year_sell_data = functions.sell_chart_data(365, 'month')
                label = 'سال گذشته'
                return render(request, 'dashboard_app/charts/order_sell_chart.html',
                              {'label': label, 'order_data': last_year_order_data, 'sell_data': last_year_sell_data})
            else:
                raise Http404()
        else:
            raise Http404()


class AllOrderChart(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                last_day_order_data = functions.all_order_chart_data()
                last_day_sell_data = functions.all_sell_chart_data()
                years = range(Order.objects.first().year, Order.objects.last().year + 2)
                label = 'تمام سفارشات'
                return render(request, 'dashboard_app/charts/order_sell_chart.html',
                              {'years': years, 'label': label, 'order_data': last_day_order_data,
                               'sell_data': last_day_sell_data})
            else:
                raise Http404()
        else:
            raise Http404()


class YearChart(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                year = request.GET.get('year')
                years = range(Order.objects.first().year, Order.objects.last().year + 2)
                if year:
                    last_year_order_data = functions.index_order_count_chart(int(year))
                    last_year_sell_data = functions.index_sell_amount_chart(int(year))
                    return render(request, 'dashboard_app/charts/order_sell_chart.html',
                                  {'years': years, 'order_data': last_year_order_data,
                                   'sell_data': last_year_sell_data})
                last_year_order_data = functions.order_chart_data(365, 'month')
                last_year_sell_data = functions.sell_chart_data(365, 'month')
                label = 'سال گذشته'
                return render(request, 'dashboard_app/charts/order_sell_chart.html',
                              {'years': years, 'label': label, 'order_data': last_year_order_data,
                               'sell_data': last_year_sell_data})
            else:
                raise Http404()
        else:
            raise Http404()


class ProductSaleStatistics(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                products = Product.objects.all()
                slug = request.GET.get('slug')
                date = request.GET.get('date')
                if slug and date:
                    product = get_object_or_404(Product, slug=slug)
                    if date == '365':
                        year_order_data = functions.product_last_year_order_count(product)
                        year_sell_date = functions.product_last_year_sell_amount(product)
                        return render(request, 'dashboard_app/charts/product_sell_chart.html',
                                      {'products': products, 'year_order_data': year_order_data,
                                       'year_sell_data': year_sell_date})
                    if date == '30':
                        month_order_data = functions.product_last_month_order_count(product)
                        month_sell_date = functions.product_last_month_sell_amount(product)
                        return render(request, 'dashboard_app/charts/product_sell_chart.html',
                                      {'products': products, 'month_order_data': month_order_data,
                                       'month_sell_data': month_sell_date})
                    if date == '7':
                        week_order_data = functions.product_last_week_order_count(product)
                        week_sell_date = functions.product_last_week_sell_amount(product)
                        return render(request, 'dashboard_app/charts/product_sell_chart.html',
                                      {'products': products, 'week_order_data': week_order_data,
                                       'week_sell_data': week_sell_date})
                    if date == '1':
                        day_order_data = functions.product_last_day_order_count(product)
                        day_sell_date = functions.product_last_day_sell_amount(product)
                        return render(request, 'dashboard_app/charts/product_sell_chart.html',
                                      {'products': products, 'day_order_data': day_order_data,
                                       'day_sell_data': day_sell_date})
                    else:
                        all_order_data = functions.product_all_order_count(product)
                        all_sell_date = functions.product_all_sell_amount(product)
                        return render(request, 'dashboard_app/charts/product_sell_chart.html',
                                      {'products': products, 'all_order_data': all_order_data,
                                       'all_sell_data': all_sell_date})
                else:
                    return render(request, 'dashboard_app/charts/product_sell_chart.html', {'products': products})
            else:
                raise Http404()
        else:
            raise Http404()


class ProductAttributeSaleStatistics(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                products = Product.objects.all()
                product_id = request.GET.get('id')
                day = request.GET.get('day')
                if product_id and day:
                    if day == 'all':
                        orders = OrderItem.objects.filter(product__id=int(product_id),
                                                          order__order_status__in=functions.order_status).values(
                            'product', 'size',
                            'color').annotate(
                            total_sell_amount=Sum(F('price') * F('quantity')),
                            order_count=Count('id')
                        )
                    else:
                        orders = OrderItem.objects.filter(created_at__gte=(today - timedelta(days=int(day))),
                                                          product__id=int(product_id),
                                                          order__order_status__in=functions.order_status).values(
                            'product', 'size',
                            'color').annotate(
                            total_sell_amount=Sum(F('price') * F('quantity')),
                            order_count=Count('id')
                        )
                    labels = []
                    data = []
                    for order in orders:
                        labels.append(f"{order['color']}-{order['size']}")
                        data.append(order['total_sell_amount'])
                    return render(request, 'dashboard_app/charts/product_attribute_sell_chart.html',
                                  {'labels': labels, 'data': data, 'products': products})
                else:
                    return render(request, 'dashboard_app/charts/product_attribute_sell_chart.html',
                                  {'products': products})
            else:
                raise Http404()
        else:
            raise Http404()


class ProductComparisonSellChart(View):
    def get(self, request):
        products = Product.objects.all()
        product_title_1 = request.GET.get('title1')
        product_title_2 = request.GET.get('title2')
        if product_title_1 and product_title_2:
            data_1 = functions.product1_comparison_last_year(product_title_1)
            data_2 = functions.product2_comparison_last_year(product_title_2)
            return render(request, 'dashboard_app/charts/product_comparison_sell_chart.html',
                          {'products': products, 'data_1': data_1, 'data_2': data_2, 'title1': product_title_1,
                           'title2': product_title_2})
        else:
            return render(request, 'dashboard_app/charts/product_comparison_sell_chart.html', {'products': products})


class UserSignupChart(View):
    def get(self, request):
        years = range(Order.objects.first().year, Order.objects.last().year + 2)
        day = request.GET.get('day')
        if day:
            if day == '1':
                value = 'hour'
                user_data_list = functions.user_signup_chart(int(day), value)
                return render(request, 'dashboard_app/charts/user_signup_chart.html',
                              {'years': years, 'hour_data': user_data_list})
            elif day == '7' or day == '30':
                value = 'day'
                user_data_list = functions.user_signup_chart(int(day), value)
                return render(request, 'dashboard_app/charts/user_signup_chart.html',
                              {'years': years, 'day_data': user_data_list})
            elif day == '365':
                value = 'month'
                user_data_list = functions.user_signup_chart(int(day), value)
                return render(request, 'dashboard_app/charts/user_signup_chart.html',
                              {'years': years, 'month_data': user_data_list})
            elif day == 'all':
                user_data = User.objects.filter().values('year').annotate(
                    count=Count('id'),
                ).order_by('year')
                user_data_list = list(user_data)
                return render(request, 'dashboard_app/charts/user_signup_chart.html',
                              {'years': years, 'year_data': user_data_list})
            else:
                user_data = User.objects.filter(year=day).values('month').annotate(
                    count=Count('id'),
                ).order_by('month')
                user_data_list = list(user_data)
                return render(request, 'dashboard_app/charts/user_signup_chart.html',
                              {'years': years, 'one_year_data': user_data_list})
        user_data = User.objects.filter().values('year').annotate(
            count=Count('id'),
        ).order_by('year')
        user_data_list = list(user_data)
        return render(request, 'dashboard_app/charts/user_signup_chart.html',
                      {'years': years, 'year_data': user_data_list})
