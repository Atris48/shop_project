from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
from index_app.models import ReadableArticles
from product_app.models import Product, ProductSpecialOffer, IndexSlideAds, IndexMobileBoxAds, IndexDesktopBoxAds, \
    ChosenProduct


class Index(View):
    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        all_products = Product.objects.filter(is_published=True).order_by('-is_available')[:10]
        recent_products = Product.objects.filter(is_published=True).order_by('-is_available', '-created_at')[:8]
        most_buy = Product.objects.filter(is_published=True).order_by('-is_available').order_by('-sell_count')[:8]
        special_offers = ProductSpecialOffer.objects.first().products.order_by('-is_available')
        chosen_lists = ChosenProduct.objects.all()
        slide_banners = IndexSlideAds.objects.all()
        readable_articles = ReadableArticles.objects.first().articles.all()
        mobile_ads = IndexMobileBoxAds.objects.all()[:2]
        desktop_ads = IndexDesktopBoxAds.objects.all()[:2]
        return render(request, 'index_app/index.html',
                      {'recent_products': recent_products, 'special_offers': special_offers,
                       'slide_banners': slide_banners, 'readable_articles': readable_articles,
                       'mobile_ads': mobile_ads, 'desktop_ads': desktop_ads,
                       'all_products': all_products, 'most_buy': most_buy, 'chosen_lists': chosen_lists})


def return_terms(request):
    return render(request, 'index_app/return-terms.html')


def terms_and_rules(request):
    return render(request, 'index_app/rules-and-terms.html')
