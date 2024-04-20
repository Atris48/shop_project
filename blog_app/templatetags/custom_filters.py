from django import template

register = template.Library()


@register.filter()
def get_active_orders(orders):
    count = 0
    for order in orders:
        if order.order_status in ['آماده سازی', 'آماده شده']:
            count += 1
    return count


@register.filter()
def get_send_orders(orders):
    count = 0
    for order in orders:
        if order.order_status == 'ارسال شده':
            count += 1
    return count


@register.filter()
def get_referral_orders(orders):
    count = 0
    for order in orders:
        if order.order_status == 'مرجوع شده':
            count += 1
    return count


@register.filter()
def minus(value, value2):
    return value - value2


@register.filter()
def sum_sell(dictionary):
    total = 0
    for item in dictionary:
        total += item['sell_mount']
    return total


@register.filter()
def total_order_count(dictionary):
    total = 0
    for item in dictionary:
        total += item['order_count']
    return total
