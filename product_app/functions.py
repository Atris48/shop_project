from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect

from product_app.cart_module import Cart
from product_app.models import Product, ProductSpecialOffer


def get_product_sizes(products):
    sizes = []
    for product in products:
        if product.has_attribute():
            for attribute in product.attribute.all():
                if attribute.size:
                    if attribute.size.size_name not in sizes:
                        sizes.append(attribute.size.size_name)
    return sizes


def get_product_colors(products):
    colors = []
    for product in products:
        if product.has_attribute():
            for attribute in product.attribute.all():
                if attribute.color:
                    if attribute.color.fa_title not in colors:
                        colors.append(attribute.color.fa_title)
    return colors


def filter_products(request, queryset):
    sizes = request.GET.getlist('size')
    colors = request.GET.getlist('color')
    is_special = request.GET.get('special')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')
    all_products = queryset
    if sizes and colors:
        all_products = all_products.filter(
            Q(attribute__size__size_name__in=sizes) & Q(attribute__color__en_title__in=colors)).distinct()
    else:
        if sizes:
            all_products = all_products.filter(attribute__size__size_name__in=sizes).distinct()
        if colors:
            all_products = all_products.filter(attribute__color__en_title__in=colors).distinct()
    if min_price and max_price:
        all_products = all_products.filter(
            Q(price__gte=min_price, price__lte=max_price) | Q(discounted_price__gte=min_price,
                                                              discounted_price__lte=max_price))
    if is_special == 'on':
        all_products = ProductSpecialOffer.objects.first().products.filter(
            title__in=all_products.values_list('title')).order_by(
            '-sell_count')
    if sort:
        if sort in ['-created_at', '-price', 'price']:
            all_products = all_products.order_by(sort)
    return all_products


def filter_special_offer_product(request, queryset):
    sizes = request.GET.getlist('size')
    colors = request.GET.getlist('color')
    sort = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    special_offers = queryset
    if colors and sizes:
        special_offers = special_offers.filter(
            Q(attribute__color__en_title__in=colors) & Q(attribute__size__size_name__in=sizes)).distinct()
    else:
        if sizes:
            special_offers = special_offers.filter(attribute__size__size_name__in=sizes).distinct()
        if colors:
            special_offers = special_offers.filter(attribute__color__en_title__in=colors).distinct()
    if min_price and max_price:
        special_offers = special_offers.filter(discounted_price__gte=min_price, discounted_price__lte=max_price)
    if sort:
        if sort in ['-created_at', '-discounted_price', 'discounted_price']:
            special_offers = special_offers.order_by(sort)
    return special_offers


def cart_add_with_color_size(quantity, attribute, request, product, color, size):
    if int(quantity) <= attribute.inventory:
        if int(quantity) > 0:
            cart = Cart(request)
            cart.add(request, product, int(quantity), attribute.inventory, color, size)
            return redirect('product_detail', product.slug)
        else:
            messages.error(request, 'تعداد درخواستی نمیتواند کمتر از 1 باشد')
            return redirect('product_detail', product.slug)
    else:
        messages.error(request, 'تعداد درخواستی شما بیش از موجودی محصول میباشد')
        return redirect('product_detail', product.slug)

