from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
from .cart_module import Cart
from .functions import get_product_sizes, get_product_colors, filter_products, filter_special_offer_product, \
    cart_add_with_color_size
from product_app.models import Product, ProductSpecialOffer, ProductCategory, ChosenProduct, ProductAttribute
from django.db.models import Q


class ProductDetail(View):
    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        sizes = []
        colors = []
        if product.has_attribute():
            for object in product.attribute.all():
                if object.size:
                    if object.size.size_name not in sizes and object.inventory != 0:
                        sizes.append(object.size.size_name)
                if object.color:
                    if object.color.fa_title not in colors and object.inventory != 0:
                        colors.append(object.color.fa_title)
        same_products = Product.objects.filter(
            Q(title__in=product.title) | Q(category__in=product.category.all())
        ).exclude(slug=slug).distinct()
        return render(request, 'product_app/product-detail.html',
                      {'product': product, 'sizes': sizes, 'colors': colors, 'same_products': same_products})

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.product_is_available:
            quantity = request.POST.get('quantity')
            if product.is_available:
                if product.inventory != None or product.attributes.count() > 0:
                    if product.inventory == None:
                        color = request.POST.get('color', None)
                        if not color:
                            color = None
                        size = request.POST.get('size')
                        if not size:
                            size = None
                        if ProductAttribute.objects.filter(product=product, size__size_name=size,
                                                           color__fa_title=color).exists():
                            attribute = ProductAttribute.objects.filter(product=product, color__fa_title=color,
                                                                        size__size_name=size).first()
                            if attribute.inventory != 0:
                                return cart_add_with_color_size(quantity, attribute, request, product, color, size)
                            else:
                                messages.error(request, 'محصول با مشخصات انتخابی ناموجود میباشد')
                                return redirect('product_detail', slug)
                        else:
                            messages.error(request, 'مشخصات انتخابی محصول یافت نشد')
                            return redirect('product_detail', product.slug)
                    else:
                        cart = Cart(request)
                        cart.add(request, product, quantity, product.inventory)
                        return redirect('product_detail', product.slug)
                else:
                    messages.error(request, 'درحال حاضر امکان ثبت سفارش این محصول نمیباشد')
                    return redirect('product_detail', slug)
            else:
                messages.error(request, 'محصول ناموجود میباشد')
                return redirect('product_detail', slug)
        else:
            messages.error(request, 'محصول ناموجود میباشد')
            return redirect('product_detail', slug)


class GetProductColors(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        size = request.GET.get('size')
        attributes = ProductAttribute.objects.filter(product=product, size__size_name=size, inventory__gt=0).all()
        colors = []
        en_titles = []
        for object in attributes:
            if object.color.fa_title not in colors:
                colors.append(object.color.fa_title)
                en_titles.append(object.color.en_title)
        return JsonResponse({'colors': colors, 'en_titles': en_titles})


class AllProductList(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        queryset = Product.objects.filter(is_published=True)
        sizes = get_product_sizes(queryset)
        colors = get_product_colors(queryset)
        all_products = filter_products(request, queryset)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_products, 18)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'product_app/product-list.html', {'products': page_obj, 'sizes': sizes,
                                                                 'colors': colors})


class ChosenProductDetail(View):
    chosen_products_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request, slug):
        object = get_object_or_404(ChosenProduct, slug=slug)
        queryset = object.products.all()
        sizes = get_product_sizes(queryset)
        colors = get_product_colors(queryset)
        all_products = filter_products(request, queryset)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_products, 18)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'product_app/product-list.html', {'products': page_obj, 'sizes': sizes,
                                                                 'colors': colors})


class MostBuyProductList(View):
    most_buy_products_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        queryset = Product.objects.filter(is_published=True).order_by('-sell_count').all()
        sizes = get_product_sizes(queryset)
        colors = get_product_colors(queryset)
        all_products = filter_products(request, queryset)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_products, 18)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'product_app/product-list.html', {'products': page_obj, 'sizes': sizes,
                                                                 'colors': colors})


class ProductCategoryDetail(View):
    category_products_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request, slug):
        product_category = get_object_or_404(ProductCategory, slug=slug)
        queryset = Product.objects.filter(is_published=True, is_available=True, category=product_category).order_by(
            '-id')
        sizes = get_product_sizes(queryset)
        colors = get_product_colors(queryset)
        all_products = filter_products(request, queryset)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_products, 18)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'product_app/product-list.html', {'products': page_obj, 'sizes': sizes,
                                                                 'colors': colors})


class SpecialOfferProductList(View):
    offer_products_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        queryset = ProductSpecialOffer.objects.first().products.all()
        sizes = get_product_sizes(queryset)
        colors = get_product_colors(queryset)
        special_offers = filter_special_offer_product(request, queryset)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(special_offers, 18)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'product_app/product-list.html', {'products': page_obj, 'sizes': sizes,
                                                                 'colors': colors})


class ProductSearchSuggest(View):
    def get(self, request):
        q = request.GET.get('q')
        result = []
        if q:
            products = Product.objects.filter(is_published=True, is_available=True, title__icontains=q)[:5]
            if products:
                for product in products:
                    result.append(product.title)
        return JsonResponse({"result": result})


class ProductSearchResult(View):
    search_products_ips = {}

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        q = request.GET.get('q')
        if q:
            queryset = Product.objects.filter(is_published=True, is_available=True, title__icontains=q).order_by('-id')
        else:
            queryset = Product.objects.filter(is_published=True).order_by('-id')
        sizes = get_product_sizes(queryset)
        colors = get_product_colors(queryset)
        all_products = filter_products(request, queryset)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_products, 18)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'product_app/product-list.html', {'products': page_obj, 'sizes': sizes,
                                                                 'colors': colors})


class AddRemoveFavorite(View):
    @method_decorator(login_required, name='dispatch', )
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user
        if user in product.favorites.all():
            product.favorites.remove(user)
            product.save()
            return JsonResponse({'message': 'remove'})
        product.favorites.add(user)
        product.save()
        return JsonResponse({'message': 'add'})
