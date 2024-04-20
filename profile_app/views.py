import jdatetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from account_app.models import User
from order_app.models import Order, OrderReferral, FactorDiscount
from product_app.models import Product
from profile_app.forms import UserEditForm, UserDataForm, AddAddressForm
from django.http import HttpResponseForbidden

from profile_app.functions import remove_notif
from profile_app.models import Notification, Address, Prize


def profile_desktop_menu(request, phone):
    user = get_object_or_404(User, phone=phone)
    return render(request, 'profile_includes/desktop_menu.html',
                  {"user": user})


def profile_mobile_menu(request, phone):
    user = get_object_or_404(User, phone=phone)
    return render(request, 'profile_includes/mobile_menu.html',
                  {"user": user})


def profile_mobile_header_menu(request, phone):
    user = get_object_or_404(User, phone=phone)
    return render(request, 'profile_includes/mobile_header_menu.html',
                  {"user": user})


class UserProfileDashboard(View):
    profile_dashboard = {}

    # @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            return render(request, 'profiles_app/profile-dashboard.html', {'user': user})
        else:
            return HttpResponseForbidden()


class UserProfileFavorite(View):
    GET_profile_fav = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            return render(request, 'profiles_app/profile-favorite.html', {'user': user})
        else:
            return HttpResponseForbidden()

    def post(self, request, phone):
        if request.user.is_authenticated:
            user = get_object_or_404(User, phone=phone)
            slug = request.POST.get('slug')
            product = get_object_or_404(Product, slug=slug)
            if request.user == user or request.user.is_admin:
                product.favorites.remove(user)
                return redirect('user_profile_favorites', phone=phone)
            else:
                return HttpResponseForbidden()
        else:
            return redirect('user_login')


class UserProfileOrders(View):
    GET_profile_order = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            orders = user.orders.order_by('-created_at')
            page_num = request.GET.get('page', 1)
            paginator = Paginator(orders, 10)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'profiles_app/profile-orders.html', {'user': user, 'orders': page_obj})
        else:
            return HttpResponseForbidden()


class ReferralOrder(View):
    GET_profile_referral = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, unique_id):
        order = get_object_or_404(Order, unique_id=unique_id)
        if order.user == request.user or request.user.is_admin:
            if order.is_valid_for_referral():
                return render(request, 'profiles_app/profile-referral-order.html', {'order': order})
            else:
                messages.error(request, 'از سفارش شما 24 ساعت گذشته است')
                return redirect('user_profile_orders', order.user.phone)
        else:
            return HttpResponseForbidden()

    @method_decorator(login_required, name='dispatch', )
    def post(self, request, unique_id):
        order = get_object_or_404(Order, unique_id=unique_id)
        if order.user == request.user or request.user.is_admin:
            if not OrderReferral.objects.filter(order=order).exists():
                if order.is_valid_for_referral():
                    reason = request.POST.get('reason')
                    if reason:
                        image = request.FILES.get('image')
                        if image:
                            OrderReferral.objects.create(order=order, reason=reason, image=image)
                            messages.success(request,
                                             'درخواست شما با موفقیت ثبت شد، در اسرع وقت با شما تماس گرفته خواهد شد')
                            return redirect('user_profile_orders', order.user.phone)
                        else:
                            OrderReferral.objects.create(order=order, reason=reason)
                            messages.success(request,
                                             'درخواست شما با موفقیت ثبت شد، در اسرع وقت با شما تماس گرفته خواهد شد')
                            return redirect('user_profile_orders', order.user.phone)
                    else:
                        messages.error(request, 'لطفا دلیل مرجوع کردن را بنویسید')
                        return redirect('user_profile_order_referral', order.unique_id)
                else:
                    messages.error(request, 'از سفارش شما 24 ساعت گذشته است')
                    return redirect('user_profile_orders', order.user.phone)
            else:
                messages.error(request, 'درخواست شما برای این سفارش ثبت شده است')
                return redirect('user_profile_orders', order.user.phone)
        else:
            return HttpResponseForbidden()


class UserProfileOrderDetail(View):
    GET_profile_order_detail = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, unique_id):
        order = get_object_or_404(Order, unique_id=unique_id)
        if request.user == order.user or request.user.is_admin:
            return render(request, 'profiles_app/profile-orders-detail.html', {'order': order})
        else:
            return HttpResponseForbidden()


class UserProfileNotification(View):
    GET_profile_notif = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            notifications = Notification.objects.filter(Q(user=user) | Q(user=None)).order_by('-created_at')
            remove_notif(notifications)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(notifications, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'profiles_app/profile-notification.html',
                          {'user': user, 'notifications': page_obj})
        else:
            return HttpResponseForbidden()


class UserProfileAddress(View):
    GET_profile_address = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            form = AddAddressForm()
            return render(request, 'profiles_app/profile-address.html', {'user': user, 'form': form})
        else:
            return HttpResponseForbidden()

    @method_decorator(login_required, name='dispatch', )
    def post(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            address_id = request.POST.get('address_id')
            if address_id:
                address = get_object_or_404(Address, id=address_id)
                if user == address.user or request.user.is_admin:
                    address.address = request.POST.get('old_address', address.address)
                    address.city = request.POST.get('city', address.city)
                    address.state = request.POST.get('state', address.state)
                    address.plaque = request.POST.get('plaque', address.plaque)
                    address.unit = request.POST.get('unit', address.unit)
                    address.postal_code = request.POST.get('postal_code', address.postal_code)
                    address.save()
                    return render(request, 'profiles_app/profile-address.html', {'user': user})
                else:
                    return HttpResponseForbidden()
            else:
                return render(request, 'profiles_app/profile-address.html', {'user': user})
        else:
            return HttpResponseForbidden()


class AddAddress(View):
    @method_decorator(login_required, name='dispatch', )
    def post(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            if user.address_set.count() < 5:
                form = AddAddressForm(data=request.POST)
                if form.is_valid():
                    address_obj = form.save(commit=False)
                    address_obj.user = user
                    address_obj.save()
                    return redirect('user_profile_address', phone)
                else:
                    messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
                    return redirect('user_profile_address', phone)
            else:
                messages.error(request, 'شما حداکثر میتوانید 5 آدرس داشته باشید')
                return redirect('user_profile_address', phone)
        else:
            return HttpResponseForbidden()


class DeleteAddress(View):
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, id):
        user = request.user
        address = get_object_or_404(Address, id=id)
        if address.user == user or request.user.is_admin:
            address.delete()
            return redirect('user_profile_address', address.user.phone)
        else:
            return HttpResponseForbidden()


class UserEditProfile(View):
    GET_profile_edit = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            form = UserDataForm(instance=user)
            edit_form = UserEditForm(instance=user)
            return render(request, 'profiles_app/profile-edit.html', {'form': form, 'edit_form': edit_form})
        else:
            return HttpResponseForbidden()

    def post(self, request, phone):
        if request.user.is_authenticated:
            user = get_object_or_404(User, phone=phone)
            if request.user == user or request.user.is_admin:
                if user.birthdate:
                    return redirect('user_edit_profile', phone)
                else:
                    form = UserDataForm(instance=user)
                    edit_form = UserEditForm(instance=user, data=request.POST)
                    if edit_form.is_valid():
                        user.birthdate = edit_form.cleaned_data.get('birthdate')
                        user.save()
                        messages.success(request, 'تاریخ تولد شما با موفقیت ثبت شد')
                        return render(request, 'profiles_app/profile-edit.html', {'form': form, 'edit_form': edit_form})
                    else:
                        return render(request, 'profiles_app/profile-edit.html', {'form': form, 'edit_form': edit_form})
            else:
                return HttpResponseForbidden()
        else:
            return redirect('user_login')


class UserChangePassword(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            return render(request, 'profiles_app/profile_change_password.html')
        else:
            return HttpResponseForbidden()

    def post(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            password = request.POST.get("password")
            confirm_password = request.POST.get('confirm_password')
            if password and confirm_password:
                if password == confirm_password:
                    if len(password) >= 8:
                        user.set_password(password)
                        user.save()
                        messages.success(request, 'رمز عبور شما تغییر یافت')
                        return redirect('user_change_password', user.phone)
                    else:
                        messages.error(request, 'رمز عبور باید حداقل 8 کاراکتر باشد')
                        return redirect('user_change_password', user.phone)
                else:
                    messages.error(request, 'رمز عبور و نکرار رمز عبور یکسان نمیباشد')
                    return redirect('user_change_password', user.phone)
            else:
                messages.error(request, 'لطفا اطلاعات را به درستی وارد کنید')
                return redirect('user_change_password', user.phone)
        else:
            return HttpResponseForbidden()


class UseGetPrize(View):

    # @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            prizes = Prize.objects.all()
            user_active_discount = FactorDiscount.objects.filter(user=user)
            return render(request, 'profiles_app/profile-prizes.html',
                          {'prizes': prizes, 'user_active_discount': user_active_discount})
        else:
            return HttpResponseForbidden()

    def post(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if request.user == user or request.user.is_admin:
            prize_id = request.POST.get("prize_id")
            prize = get_object_or_404(Prize, id=int(prize_id))
            if user.prize_amount >= prize.amount:
                discount = prize.discount
                user.prize_amount -= prize.amount
                user.save()
                discount.user.add(user)
                messages.success(request, 'کد تخفیف برای شما ثبت شد')
                return redirect('user_profile_prizes', user.phone)
            else:
                messages.error(request, 'امتیاز شما به اندازه ی کافی نمیباشد')
                return redirect('user_profile_prizes', user.phone)

        else:
            return HttpResponseForbidden()
