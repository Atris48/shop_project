from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from product_app.models import ProductAttribute

register = template.Library()


@register.filter()
def get_query_params(querydict):
    params = {}
    for key, values in querydict.lists():
        cleaned_key = key.strip()
        cleaned_values = [value.strip() for value in values]
        params[cleaned_key] = cleaned_values
    return params


@register.filter()
def get_query_params_for_sorting(querydict):
    params = {}
    for key, values in querydict.lists():
        if key.lower() == 'sort':
            continue
        cleaned_key = key.strip()
        cleaned_values = [value.strip() for value in values]
        params[cleaned_key] = cleaned_values
    return params


# @register.filter()
# def get_query_param(request):
#     query_param = ''
#     for key, value in request.GET.lists():
#         query_param += f"{key}={value}&"
#     return query_param[:-1]


@register.filter()
def get_en_title(fa_title):
    attribute = ProductAttribute.objects.filter(color__fa_title=fa_title).first()
    return attribute.color.en_title


@register.filter()
def get_list(param, value):
    values = param.getlist(value)
    return values


@register.filter()
def get_public_comments(queryset, request):
    comments = queryset.filter(is_publish=True).order_by('-created_at').prefetch_related('likes').prefetch_related(
        'dislikes').all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(comments, 10)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    page_obj.paginator.page_range
    return page_obj


@register.filter()
def get_public_comments_count(queryset):
    return queryset.filter(is_publish=True).count()

@register.filter()
def check_user_buy_product(product, user):
    orders = user.orders.all()
    for order in orders:
        for item in order.items.all():
            if product == item.product:
                return True
    return False
