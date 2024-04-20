from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
from .functions import get_client_ip
from .models import Article, BlogAds, ArticleChoose, ArticleCategory
from django.db.models import Q


class BlogIndex(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        articles = Article.objects.filter(is_published=True).prefetch_related('categories').order_by('-id')[:4]
        most_view_articles = Article.objects.filter(is_published=True).order_by('-visit_count').prefetch_related(
            'categories')[:4]
        ads_image = BlogAds.objects.first()
        chosen_articles = ArticleChoose.objects.first()
        return render(request, 'blog_app/blog.html', {'articles': articles,
                                                      'most_view': most_view_articles,
                                                      'ads_image': ads_image, 'chosen_articles': chosen_articles})


class BlogDetail(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        user_ip = get_client_ip(request)
        if user_ip not in article.unique_visitors.split(','):
            article.unique_visitors += f"{user_ip},"
            article.visit_count += 1
            article.save()
        same_article = Article.objects.filter(
            Q(title__in=article.title.split(' ')) |
            Q(categories__in=article.categories.all())
        ).exclude(slug=slug).prefetch_related('categories').distinct()[:8]
        return render(request, 'blog_app/blog-detail.html', {'article': article, 'same_article': same_article})


class ArticleList(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        articles = Article.objects.filter(is_published=True) \
            .prefetch_related('categories').order_by('-id')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(articles, 9)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'blog_app/blog-list.html', {'articles': page_obj})


class CategoryDetail(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request, slug):
        category = get_object_or_404(ArticleCategory, slug=slug)
        articles = category.article_set.filter(is_published=True).prefetch_related('categories').order_by('-id')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(articles, 9)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'blog_app/blog-list.html', {'articles': page_obj})


class SearchSuggestArticle(View):
    def get(self, request):
        q = request.GET.get('q')
        result = []
        if q:
            articles = Article.objects.filter(title__icontains=q)[:5]
            if articles:
                for article in articles:
                    result.append(article.title)
                return JsonResponse({"result": result})
        return JsonResponse({"result": result})


class SearchResultArticle(View):

    @method_decorator(ratelimit(key='user_or_ip', rate='20/m'))
    def get(self, request):
        q = request.GET.get('q')
        if q:
            articles = Article.objects.filter(is_published=True, title__icontains=q) \
                .prefetch_related('categories').order_by('-id')
        else:
            articles = Article.objects.filter(is_published=True) \
                .prefetch_related('categories').order_by('-id')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(articles, 9)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'blog_app/blog-list.html', {'articles': page_obj})
