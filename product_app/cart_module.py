from django.contrib import messages

from product_app.models import Product, ProductAttribute


# def get_inventory(product, color):
#     if product.has_attribute():
#         inventory = product.attribute.get(color__fa_title=color).inventory
#     else:
#         inventory = product.inventory
#     return inventory

def get_en_color(fa_color):
    attribute = ProductAttribute.objects.filter(color__fa_title=fa_color).first()
    return attribute.color.en_title


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            item['product'] = Product.objects.get(id=int(item['id']))
            if item['color']:
                item['en_color'] = get_en_color(item['color'])
            # inventory = get_inventory(item['product'], item['color'])
            # item['inventory'] = inventory
            item['item_total_price'] = int(item['price']) * int((item['quantity']))
            item['unique_id'] = self.unique_id_generator(item['product'].id, item['color'], item['size'])
            yield item

    def unique_id_generator(self, id, color='', size=''):
        unique_id = f'{id}-{color}-{size}'
        return unique_id

    def add(self, request, product, quantity, inventory, color='', size=''):
        unique_id = self.unique_id_generator(product.id, color, size)
        if unique_id not in self.cart:
            if product.discounted_price:
                price = product.discounted_price
            else:
                price = product.price
            self.cart[unique_id] = {'quantity': int(quantity), 'price': str(price),
                                    'color': color, 'size': size,
                                    'id': str(product.id)}
        else:
            if self.cart[unique_id]['quantity'] + int(quantity) <= int(inventory):
                self.cart[unique_id]['quantity'] += int(quantity)
            else:
                messages.error(request, 'تعداد درخواستی شما بیش از موجودی کالا میباشد')
        self.save()

    def delete_item(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def is_exist(self, unique_id):
        if unique_id in self.cart:
            return True
        return False

    def count_items(self):
        cart = self.cart.values()
        count = 0
        for item in cart:
            count += 1
        return count

    def total_price(self):
        cart = self.cart.values()
        total = 0
        for item in cart:
            total += int(item['price']) * int(item['quantity'])
        return total

    def delete_cart(self):
        del self.session['cart']

    def save(self):
        self.session.modified = True
