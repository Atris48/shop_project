import jdatetime
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
from account_app.forms import UserRegisterForm
from account_app.functions import delete_otp, create_otp, check_phone, user_login_invalid_data, login_user, expired_otp, \
    login_check_otp_invalid_data, resend_otp, wait_for_resend_otp
from account_app.models import User, Otp, Ban
from account_app.rate_limits import account_rate_limit
from django.urls import is_valid_path


class UserRegister(View):
    post_register_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        if not request.user.is_authenticated:
            form = UserRegisterForm()
            return render(request, 'account_app/register.html', {'form': form})
        else:
            return redirect('index')

    @method_decorator(account_rate_limit(post_register_ips, 4, 120))
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            delete_otp(user)
            otp = create_otp(user.phone)
            messages.success(request, 'اکانت شما ساخته شد، برای ورود کد 6 رقمی را وارد کنید')
            return redirect(reverse('login_check_otp') + f'?token={otp.token}')
        else:
            return render(request, 'account_app/register.html', {'form': form})


class UserLogin(View):
    post_login_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'account_app/login.html')
        else:
            return redirect('index')

    @method_decorator(account_rate_limit(post_login_ips, 6, 120))
    def post(self, request):
        if not request.user.is_authenticated:
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            next_page = request.POST.get('next')
            if not is_valid_path(next_page):
                next_page = 'index'
            if not Ban.objects.filter(user__phone=phone).exists():
                if check_phone(phone):
                    if User.objects.filter(phone=phone).exists():
                        user = User.objects.get(phone=phone)
                        if password == None or password == '':
                            if Otp.objects.filter(phone=user.phone).exists():
                                otp = Otp.objects.filter(phone=user.phone).last()
                                if otp.expiration_date > jdatetime.datetime.now():
                                    minute = (otp.expiration_date - jdatetime.datetime.now()).seconds // 60
                                    second = (otp.expiration_date - jdatetime.datetime.now()).seconds % 60
                                    messages.error(request, f'برای دریافت مجدد کد تایید {minute}:{second} صبر کنید')
                                    return redirect(reverse('login_check_otp') + f'?token={otp.token}&next={next_page}')
                            delete_otp(user)
                            otp = create_otp(user.phone)
                            messages.success(request, 'کد 6 رقمی را وارد کنید')
                            if next_page:
                                return redirect(reverse('login_check_otp') + f'?token={otp.token}&next={next_page}')
                            return redirect(reverse('login_check_otp') + f'?token={otp.token}')
                        else:
                            user = authenticate(username=phone, password=password)
                            if user is not None:
                                return login_user(request, user, next_page)
                            else:
                                messages.error(request, 'رمز عبور صحیح نمیباشد')
                                return redirect('user_login')
                    else:
                        message = 'کاربر با شماره وارد شده یافت نشد!!'
                        return user_login_invalid_data(request, message, next_page)
                else:
                    message = 'شماره تلفن باید 11 رقم و با 09 شروع شود'
                    return user_login_invalid_data(request, message, next_page)
            else:
                messages.error(request, 'اکانت شما توسط ادمین مسدود شده است')
                return redirect('index')
        else:
            return redirect('index')


class LoginCheckOtp(View):
    post_check_otp_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        if not request.user.is_authenticated:
            token = request.GET.get('token')
            if Otp.objects.filter(token=token).exists():
                otp = Otp.objects.get(token=token)
                exp_time = otp.expiration_date - jdatetime.datetime.now()
                return render(request, 'account_app/login-otp.html', {'exp_time': exp_time, 'token': otp.token})
            else:
                return render(request, 'account_app/login-otp.html')
        else:
            return redirect('index')

    @method_decorator(account_rate_limit(post_check_otp_ips, 6, 120))
    def post(self, request):
        if not request.user.is_authenticated:
            code = request.POST.get('code')
            token = request.POST.get('token')
            next_page = request.POST.get('next')
            if not is_valid_path(next_page):
                next_page = 'index'
            if code and token:
                if Otp.objects.filter(code=code, token=token).exists():
                    otp = Otp.objects.get(code=code, token=token)
                    if otp.expiration_date > jdatetime.datetime.now():
                        user = User.objects.get(phone=otp.phone)
                        if user.is_active:
                            delete_otp(user)
                            return login_user(request, user, next_page)
                        else:
                            delete_otp(user)
                            user.is_active = True
                            user.save()
                            return login_user(request, user, next_page)
                    else:
                        return expired_otp(request, otp, next_page)
                else:
                    message = 'کد تایید صحیح نمیباشد'
                    return login_check_otp_invalid_data(request, token, message, next_page)
            else:
                message = 'اطلاعات را به درستی وارد کنید'
                return login_check_otp_invalid_data(request, token, message, next_page)
        else:
            return redirect('index')


class UserLogout(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        logout(request)
        return redirect('index')


class ResendLoginOtp(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        token = request.GET.get('token')
        next = request.GET.get('next')
        if not is_valid_path(next):
            next = 'index'
        if Otp.objects.filter(token=token).exists():
            exp_otp = Otp.objects.get(token=token)
            if exp_otp.expiration_date < jdatetime.datetime.now():
                user = User.objects.get(phone=exp_otp.phone)
                return resend_otp(user, exp_otp.phone, request, next)
            else:
                return wait_for_resend_otp(request, exp_otp, next)
        else:
            messages.error(request, 'توکن فعال سازی معتبر نمیباشد، مجدد شماره خود را وارد کنید')
            return redirect('user_login')
