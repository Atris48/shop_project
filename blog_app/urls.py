from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.BlogIndex.as_view(), name='blog'),
    path('blog-detail/<slug:slug>', views.BlogDetail.as_view(), name='blog_detail'),
    path('article-list', views.ArticleList.as_view(), name='article_list'),
    path('category-detail/<slug:slug>', views.CategoryDetail.as_view(), name='category_detail'),
    path('search-suggest-article', views.SearchSuggestArticle.as_view(), name='search_suggest_article'),
    path('search-result-article', views.SearchResultArticle.as_view(), name='search_result_article'),
]
