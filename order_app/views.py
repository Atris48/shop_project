import datetime

from django.contrib.auth.decorators import login_required
from django.utils import timezone
import jdatetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse
from django_ratelimit.decorators import ratelimit

from order_app import functions
from order_app.models import Factor, FactorItem, Order, OrderItem, FactorDiscount
from uuid import uuid4

from order_app.rate_limits import set_address_rate_limit
from profile_app.models import Notification, Address


class FactorDetail(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request):
        factors = Factor.objects.filter(user=request.user)
        if factors.exists():
            functions.check_user_factors(factors)
            factor = Factor.objects.get(user=request.user)
            for item in factor.items.all():
                if item.get_inventory() < item.quantity:
                    item.quantity = item.get_inventory()
                    item.save()
                if item.get_inventory() == 0:
                    messages.error(request, f'محصول {item.product.title} ناموحود شده است ')
                    item.delete()
            return render(request, 'order_app/factor_detail.html', {'factor': factor})
        else:
            factor = Factor.objects.create(user=request.user)
            return render(request, 'order_app/factor_detail.html', {'factor': factor})

    @method_decorator(login_required, name='dispatch', )
    def post(self, request):
        if Factor.objects.filter(user=request.user).exists():
            factor = Factor.objects.get(user=request.user)
            functions.cart_to_factor(request, factor)
            return render(request, 'order_app/factor_detail.html', {'factor': factor})
        else:
            factor = Factor.objects.create(user=request.user, )
            functions.cart_to_factor(request, factor)
            return render(request, 'order_app/factor_detail.html', {'factor': factor})


class FactorDeleteItem(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, id):
        factor_item = get_object_or_404(FactorItem, id=id)
        if factor_item.factor.user == request.user:
            factor_item.delete()
            return redirect('factor_detail')
        else:
            return HttpResponseForbidden()


class FactorDeleteAllItem(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request):
        if request.user.factors.filter(user=request.user).exists():
            factor = request.user.factors.get(user=request.user)
            if factor.user == request.user:
                for item in factor.items.all():
                    item.delete()
                return redirect('factor_detail')
            else:
                return HttpResponseForbidden()
        else:
            factor = Factor.objects.create(user=request.user)
            return redirect('factor_detail')


class FactorItemIncreaseQuantity(View):
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, id):
        if request.user.factors.filter(user=request.user).exists():
            factor = request.user.factors.get(user=request.user)
            if factor.items.all:
                if FactorItem.objects.filter(id=id).exists():
                    item = FactorItem.objects.get(id=id)
                    if item.product.is_available:
                        if item.get_inventory() > item.quantity:
                            return functions.plus_item(item, factor)
                        else:
                            messages.error(request, 'درخواست شما بیش از موجودی کالا میباشد')
                            return JsonResponse({'status': 'fail'})
                    else:
                        item.delete()
                        messages.error(request, 'محصول مورد نظر ناموجود شده است')
                        return JsonResponse({'status': 'fail'})
                else:
                    return JsonResponse({'status': 'fail'})
            else:
                return JsonResponse({'status': 'fail'})
        else:
            factor = Factor.objects.create(user=request.user)
            return JsonResponse({'status': 'fail'})


class FactorItemDecreaseQuantity(View):
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, id):
        if request.user.factors.filter(user=request.user).exists():
            factor = request.user.factors.get(user=request.user)
            if factor.items.all:
                if FactorItem.objects.filter(id=id).exists():
                    item = FactorItem.objects.get(id=id)
                    if item.product.is_available:
                        if item.quantity > 1:
                            return functions.minus_item(item, factor)
                        else:
                            return JsonResponse({'status': 'fail'})
                    else:
                        item.delete()
                        messages.error(request, 'محصول مورد نظر ناموجود شده است')
                        return JsonResponse({'status': 'fail'})
                else:
                    return JsonResponse({'status': 'fail'})
            else:
                return JsonResponse({'status': 'fail'})
        else:
            factor = Factor.objects.create(user=request.user)
            return JsonResponse({'status': 'fail'})


class FactorAddress(View):
    POST_factor_address = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, id):
        factor = get_object_or_404(Factor, id=id)
        for item in factor.items.all():
            if item.get_inventory() == 0:
                messages.error(request, f'محصول {item.product.title} ناموحود شده است ')
                item.delete()
                return redirect('factor_detail')
        if request.user == factor.user:
            if factor.items.count() > 0:
                return render(request, 'order_app/factor-address.html', {'factor': factor})
            else:
                messages.error(request, 'سفارش شما خالی میباشد')
                return redirect('factor_detail')
        else:
            return HttpResponseForbidden()

    @method_decorator(set_address_rate_limit(POST_factor_address, 4, 120))
    @method_decorator(login_required, name='dispatch', )
    def post(self, request, id):
        factor = get_object_or_404(Factor, id=id)
        if functions.check_factor_item_inventory(factor):
            if request.user == factor.user:
                address_id = request.POST.get('address_id')
                if address_id:
                    if Address.objects.filter(id=int(address_id), user=factor.user).exists():
                        factor.address = Address.objects.get(id=address_id)
                        factor.save()
                        return redirect('factor_payment', factor.id)
                    else:
                        messages.error(request, 'آدرس انتخابی یافت نشد')
                        return redirect('factor_detail')
                else:
                    messages.error(request, 'آدرس مد نظر خود را اتخاب کنید')
                    return redirect('factor_detail')
            else:
                return HttpResponseForbidden()
        else:
            messages.error(request, 'محصولی از سفارش شما ناموجود شده است')
            return redirect('factor_detail')


class FactorPayment(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, id):
        factor = get_object_or_404(Factor, id=id)
        if functions.check_factor_item_inventory(factor):
            if factor.user == request.user:
                if factor.items.count() > 0:
                    factor.total_price = factor.get_total_price()
                    factor.save()
                    if factor.address:
                        if factor.discount:
                            if functions.check_discount(request, factor.discount, factor):
                                discounted = (factor.get_total_price() * factor.discount.percentage) / 100
                                if factor.discount.max_price:
                                    if discounted < factor.discount.max_price:
                                        factor.total_price = factor.get_total_price() - discounted
                                    else:
                                        factor.total_price = factor.get_total_price() - factor.discount.max_price
                                else:
                                    factor.total_price = factor.get_total_price() - discounted
                                factor.save()
                                return render(request, 'order_app/factor-payment.html', {'factor': factor})
                            else:
                                factor.discount = None
                                factor.save()
                        return render(request, 'order_app/factor-payment.html', {'factor': factor})
                    else:
                        messages.error(request, 'برای سفارش خود یک آدرس انتخاب کنید')
                        return redirect('factor_address', factor.id)
                else:
                    messages.error(request, 'فاکتور شما خالی است')
                    return redirect('factor_detail', factor.id)
            else:
                return HttpResponseForbidden()
        else:
            messages.error(request, 'محصولی از سفارش شما ناموجود شده است')
            return redirect('factor_detail')


class FactorDiscountView(View):
    POST_factor_discount = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def post(self, request, id):
        factor = get_object_or_404(Factor, id=id)
        code = request.POST.get('code')
        if FactorDiscount.objects.filter(code=code).exists():
            discount = FactorDiscount.objects.get(code=code)
            if factor.user not in discount.use.all():
                if functions.check_discount(request, discount, factor):
                    return functions.set_discount(request, factor, discount)
                else:
                    factor.total_price = factor.get_total_price()
                    factor.discount = None
                    factor.save()
                    return redirect('factor_payment', factor.id)
            else:
                messages.error(request, 'شما از این کد تخفیف استفاده کرده اید')
                return redirect('factor_payment', id)
        else:
            messages.error(request, 'کد تخفیف مورد نظر یافت نشد')
            return redirect('factor_payment', id)


class FactorVerifyPay(View):

    @method_decorator(login_required, name='dispatch', )
    def post(self, request, id):
        factor = get_object_or_404(Factor, id=id)
        user = factor.user
        discount = factor.discount
        now = jdatetime.datetime.now()
        if factor.discount:
            order = Order.objects.create(user=factor.user, total_price=factor.total_price,
                                         discount=factor.discount, unique_id=str(uuid4())[:5],
                                         order_status='آماده سازی', address=factor.address, year=now.year,
                                         month=now.month, day=now.day,
                                         hour=now.hour)
            discount.use.add(user)
            discount.save()
        else:
            order = Order.objects.create(user=factor.user, total_price=factor.total_price,
                                         unique_id=str(uuid4())[:5], order_status='آماده سازی', year=now.year,
                                         month=now.month, address=factor.address, day=now.day, hour=now.hour)
        user.prize_amount += (factor.total_price / 10000)
        user.save()
        for item in factor.items.all():
            OrderItem.objects.create(order=order, product=item.product, color=item.color, size=item.size,
                                     price=item.price, quantity=item.quantity)

            item.minus_inventory(item.quantity)
        notif = Notification.objects.create(title='تایید سفارش',
                                            description='کاربر عزیز با تشکر از خرید شما، سفارش شما با موفقیت ثبت شد',
                                            url=f'http://127.0.0.1:8000/user-profile-order-detail/{order.unique_id}')
        notif.user.add(request.user)
        # sms
        # sms
        factor.delete()
        return render(request, 'order_app/payment-success.html', {'order': order})
