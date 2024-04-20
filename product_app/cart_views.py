from django.http import JsonResponse
from django.views import View
from product_app.cart_module import Cart


class CartDeleteItem(View):
    def get(self, request, unique_id):
        cart = Cart(request)
        cart.delete_item(unique_id)
        return JsonResponse({'items_count': cart.count_items(), 'total_price': cart.total_price(), 'name': unique_id})
