import jdatetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from .models import *

from .rate_limits import chat_rate_limit


class CreateChatView(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request):
        if request.user.is_staff:
            messages.error(request, 'ادمین اجازه ایجاد چت ندارد')
            return redirect('dashboard')
        if Chat.objects.filter(user=request.user).exists():
            return redirect('chat_detail', request.user.phone)
        else:
            Chat.objects.create(user=request.user)
            return redirect('chat_detail', request.user.phone)


class ChatDetailView(View):
    post_chat_detail_ips = {}

    @method_decorator(chat_rate_limit(post_chat_detail_ips, 5, 120))
    @method_decorator(login_required, name='dispatch', )
    def post(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if not Chat.objects.filter(user=user).exists():
            messages.error(request, 'شما چت فعالی ندارید')
            return redirect('dashboard')
        if not request.user.phone == phone and not request.user.is_staff:
            return redirect('dashboard')
        user_text = request.POST.get('text')
        user_file = request.FILES.get('file')
        if not user_text and not user_file:
            messages.error(request, 'شما نمیتوانید پیام خالی ارسال کنید')
            return redirect('chat', phone)
        time_now = jdatetime.datetime.now()
        message_send_time = str(
            f'{time_now.time().hour}:{time_now.time().minute} {time_now.date().year}/{time_now.date().month}/{time_now.date().day}')
        if request.user.is_staff:
            if user_file:
                if user_file.size / 1000000 > 2:
                    messages.error(request, 'حجم فایل باید حداکثر دو مگابایت باشد')
                    return redirect('chat_detail', user.phone)
                if str(user_file).split('.')[-1] not in ['jpg', 'png', 'webp', 'jpeg']:
                    messages.error(request, 'فرمت فایل باید jpg,png یا webp باشد')
                    return redirect('chat_detail', user.phone)
                orginal_file_path = f'media/files/{user_file}'
                with open(orginal_file_path, 'wb+') as f:
                    for chunk in user_file.chunks():
                        f.write(chunk)

                user_dict = {"role": "admin", "content": f"/media/files/{user_file.name}", "type": "file",
                             "time": message_send_time}
            else:
                user_dict = {"role": "admin", "content": user_text, "type": "text", "time": message_send_time}
            object = Chat.objects.get(user=user)
            user_messages = object.messages_history
            user_messages.append(user_dict)
            object.is_replied = True
            object.save()
            # send_sms(user.phone, 'userticket', parm1=user.fullname)ret
            return JsonResponse(user_dict)
            # return redirect('chat_detail', user.phone)
        else:
            if user_file:
                if user_file.size / 1000000 > 2:
                    messages.error(request, 'حجم فایل باید حداکثر دو مگابایت باشد')
                    return redirect('chat_detail', user.phone)
                elif str(user_file).split('.')[-1] not in ['jpg', 'png', 'webp', 'jpeg']:
                    messages.error(request, 'فرمت فایل باید jpg,png یا webp باشد')
                    return redirect('chat_detail', user.phone)
                orginal_file_path = f'media/files/{user_file}'
                with open(orginal_file_path, 'wb+') as f:
                    for chunk in user_file.chunks():
                        f.write(chunk)
                user_dict = {"role": "user", "content": f"/media/files/{user_file.name}", "type": "file",
                             "time": message_send_time}
            else:
                user_dict = {"role": "user", "content": user_text, "type": "text",
                             "time": message_send_time}
            object = Chat.objects.get(user_id=user.id)
            user_messages = object.messages_history
            user_messages.append(user_dict)
            object.is_replied = False
            object.save()
            # send_sms('09120993133', 'adminticket', parm1=user.fullname)
            return JsonResponse(user_dict)

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        if not request.user.is_staff:
            if not Chat.objects.filter(user=request.user).exists():
                messages.error(request, 'شما چت فعالی ندارید')
                return redirect('dashboard')
        object = Chat.objects.get(user=user)
        return render(request, 'chat_app/chat/chat-detail.html', {'chat': object, 'user': user})


def remove_chat(request, pk):
    if request.user.is_staff:
        if Chat.objects.filter(user__phone=pk).exists():
            Chat.objects.get(user__phone=pk).delete()
            messages.success(request, 'چت با موفیقیت حذف شد')
            return redirect('accounts:dashboard')
        messages.error(request, 'چت موردنظر یافت نشد')
        return redirect('accounts:dashboard')
    else:
        return redirect('index')


class AdminClearChat(View):
    def get(self, request, pk):
        if request.user.is_staff:
            chat = get_object_or_404(Chat, id=pk)
            chat.messages_history.clear()
            chat.is_replied = False
            chat.save()
            messages.success(request, 'چت پاکسازی شد')
            return redirect('chat_list')
        else:
            return redirect('index')
