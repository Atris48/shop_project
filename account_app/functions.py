import random
import uuid
import jdatetime
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from account_app.models import Otp


def check_phone(phone):
    if len(phone) == 11 and phone.startswith("09"):
        return True
    else:
        False


def user_login_invalid_data(request, message, next_page=None):
    messages.error(request, message)
    if next_page:
        return redirect(reverse('user_login') + f'?next={next_page}')
    return redirect('user_login')


def delete_otp(user):
    if Otp.objects.filter(phone=user.phone).exists():
        for object in Otp.objects.filter(phone=user.phone).all():
            object.delete()


def create_otp(phone):
    random_code = random.randint(99999, 1000000)
    print('random : ', random_code)
    expiration_date = jdatetime.datetime.now() + jdatetime.timedelta(minutes=2)
    otp = Otp.objects.create(phone=phone, token=uuid.uuid4(),
                             code=random_code,
                             expiration_date=expiration_date)
    return otp


def expired_otp(request, otp, next_page=None):
    otp.delete()
    messages.error(request, 'کد اعتبار سنجی منقضی شده است')
    if next_page:
        return redirect(reverse('user_login') + f'?next={next_page}')
    return redirect('login')


def login_check_otp_invalid_data(request, token, message, next_page=None):
    messages.error(request, message)
    if next_page:
        return redirect(reverse('login_check_otp') + f'?token={token}&next={next_page}')
    return redirect(reverse('login_check_otp') + f'?token={token}')


def login_user(request, user, next_page=None):
    login(request, user)
    messages.success(request, 'خوش آمدید')
    if next_page:
        return redirect(next_page)
    return redirect('index')


def resend_otp(user, phone, request, next=None):
    delete_otp(user)
    otp = create_otp(phone)
    messages.success(request, ' کد 6 رقمی را وارد کنید')
    if next != None:
        return redirect(reverse('login_check_otp') + f'?token={otp.token}&next={next}')
    return redirect(reverse('login_check_otp') + f'?token={otp.token}')


def wait_for_resend_otp(request, otp, next=None):
    minute = (otp.expiration_date - jdatetime.datetime.now()).seconds // 60
    second = (otp.expiration_date - jdatetime.datetime.now()).seconds % 60
    messages.error(request, f'برای دریافت مجدد کد تایید {minute}:{second} صبر کنید')
    if next != None:
        return redirect(reverse('login_check_otp') + f'?token={otp.token}&next={next}')
    return redirect(reverse('login_check_otp') + f'?token={otp.token}')
