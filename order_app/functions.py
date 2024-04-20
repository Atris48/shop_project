from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

from order_app.models import FactorItem
from product_app.cart_module import Cart


def cart_to_factor(request, factor):
    cart = Cart(request)
    for item in cart:
        if FactorItem.objects.filter(factor=factor, product=item['product'], size=item['size'],
                                     color=item['color']).exists():
            factor_item = FactorItem.objects.get(factor=factor, product=item['product'], size=item['size'],
                                                 color=item['color'])
            if factor_item.get_inventory() >= (factor_item.quantity + item['quantity']):
                factor_item.price = int((factor_item.quantity + item['quantity'])) * int(item['price'])
                factor_item.quantity += item['quantity']
                factor_item.save()
                cart.delete_item(item['unique_id'])
                cart.save()
            else:
                cart.delete_item(item['unique_id'])
                cart.save()
                messages.error(request, 'درخواست شما بیش از موجود کالا میباشد')
        else:
            FactorItem.objects.create(factor=factor, product=item['product'], size=item['size'],
                                      color=item['color'], price=item['item_total_price'],
                                      quantity=item['quantity'])
            cart.delete_item(item['unique_id'])
            cart.save()


def plus_item(item, factor):
    item.quantity += 1
    if item.product.discounted_price:
        item.price += item.product.discounted_price
    else:
        item.price += item.product.price
    item.save()
    return JsonResponse(
        {"status": 'success', "item_price": item.price, "total_price": factor.get_total_price()})


def minus_item(item, factor):
    item.quantity -= 1
    if item.product.discounted_price:
        item.price -= item.product.discounted_price
    else:
        item.price -= item.product.price
    item.save()
    return JsonResponse(
        {"status": 'success', "item_price": item.price, "total_price": factor.get_total_price()})


def check_discount(request, discount, factor):
    if discount.is_expired():
        messages.error(request, 'کد تخفیف منقضی شده است')
        return False
    if discount.category.count() > 0:
        for item in factor.items.all():
            category = discount.is_valid_for_category(item.product.category.all())
            if category != True:
                messages.error(request, f'دسته بندی {category} شامل این کد تخفیف نمیباشد ')
                return False
    if discount.products.count() > 0:
        for item in factor.items.all():
            if discount.is_valid_for_products(item.product) == False:
                messages.error(request, f'محصول {item.product.title} شامل این کد تخفیف نمیباشد ')
                return False
    if discount.user.count() > 0:
        if not discount.is_valid_for_user(factor.user):
            messages.error(request, 'این کد تخفیف برای شما در نظر گرفته نشده است')
            return False
    return True


def set_discount(request, factor, discount):
    discounted = (factor.get_total_price() * discount.percentage) / 100
    if discount.max_price:
        if discounted < discount.max_price:
            factor.total_price = factor.get_total_price() - discounted
        else:
            factor.total_price = factor.get_total_price() - discount.max_price
    else:
        factor.total_price = factor.get_total_price() - discounted
    factor.discount = discount
    factor.save()
    messages.success(request, 'کد تخفیف اعمال شد')
    return redirect('factor_payment', factor.id)


def check_user_factors(factors):
    if factors.count() > 1:
        for object in factors.all()[0:factors.count() - 1]:
            object.delete()


def check_factor_item_inventory(factor):
    unavailable = 0
    for item in factor.items.all():
        if item.get_inventory() == 0:
            item.delete()
            unavailable += 1
    if unavailable == 0:
        return True
    else:
        return False
