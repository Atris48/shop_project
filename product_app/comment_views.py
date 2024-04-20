from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from product_app.models import Product, ProductComment


class ProductAddComment(View):
    def post(self, request, slug):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, slug=slug)
            title = request.POST.get('title')
            suggest = request.POST.get('suggest')
            text = request.POST.get('text')
            if title and suggest and text:
                if len(title) < 100 and suggest in ['پیشنهاد میکنم', 'پیشنهاد نمیکنم']:
                    if product.check_user_buy_product(request.user):
                        if request.user.is_admin:
                            ProductComment.objects.create(product=product, user=request.user, title=title,
                                                          opinion=suggest,
                                                          text=text, is_publish=True)
                            messages.success(request, 'دیدگاه شما ثبت شد')
                            return redirect('product_detail', slug)
                        else:
                            ProductComment.objects.create(product=product, user=request.user, title=title,
                                                          opinion=suggest,
                                                          text=text)
                            messages.success(request, 'دیدگاه شما ثبت شد')
                            return redirect('product_detail', slug)
                    else:
                        messages.error(request, 'شما محصول را خریداری نکرده اید')
                        return redirect('product_detail', slug)
                else:
                    messages.error(request, 'عنوان باید کمتر از 100 حرف باشد')
                    return redirect('product_detail', slug)
            else:
                messages.error(request, 'اطلاعات را کامل ارسال کنید')
                return redirect('product_detail', slug)
        else:
            return redirect('user_login')


class ProductRemoveComment(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            comment = get_object_or_404(ProductComment, id=id)
            if request.user.is_admin or request.user == comment.user:
                comment.delete()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseForbidden()
        else:
            return redirect('user_login')


class CommentLikeView(View):
    def post(self, request, id):
        if request.user.is_authenticated:
            comment = get_object_or_404(ProductComment, id=id)
            ProductComment.objects.prefetch_related()
            comment.likes.add(request.user)
            if comment.dislikes.filter(phone=request.user.phone).exists():
                comment.dislikes.remove(request.user)
            comment.save()
            return JsonResponse({"like_count": comment.likes.count(), 'dislike_count': comment.dislikes.count()})
        else:
            return JsonResponse({'status': 'fail'})


class CommentDislikeView(View):
    def post(self, request, id):
        if request.user.is_authenticated:
            comment = get_object_or_404(ProductComment, id=id)
            comment.dislikes.add(request.user)
            if comment.likes.filter(phone=request.user.phone).exists():
                comment.likes.remove(request.user)
            comment.save()
            return JsonResponse({"like_count": comment.likes.count(), 'dislike_count': comment.dislikes.count()})
        else:
            return JsonResponse({'status': 'fail'})
