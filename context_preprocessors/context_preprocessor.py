from blog_app.models import ArticleCategory
from product_app.models import ProductCategory
from product_app.cart_module import Cart


def context_categories(request):
    nav_categories = ArticleCategory.objects.all()
    return {"nav_categories": nav_categories}


def product_categories(request):
    product_categories = ProductCategory.objects.all()
    return {"product_categories": product_categories}


def cart(request):
    return {'cart': Cart(request)}
