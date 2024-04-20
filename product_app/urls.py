from django.urls import path
from . import views, cart_views
from . import comment_views

urlpatterns = [
    path('product-detail/<slug:slug>', views.ProductDetail.as_view(), name='product_detail'),
    path('get-product-colors/<slug:slug>', views.GetProductColors.as_view(), name='get_product_colors'),
    path('all-products', views.AllProductList.as_view(), name='all_product'),
    path('most-buy-products', views.MostBuyProductList.as_view(), name='most_buy_products'),
    path('chosen-products/<slug:slug>', views.ChosenProductDetail.as_view(), name='chosen_products'),
    path('producct-category-detail/<slug:slug>', views.ProductCategoryDetail.as_view(), name='product_category_detail'),
    path('special-offer-products', views.SpecialOfferProductList.as_view(), name='special_offers'),
    path('product-search-suggest', views.ProductSearchSuggest.as_view()),
    path('product-search-result', views.ProductSearchResult.as_view(), name='product_search_result'),
    path('add-remove-favorite/<slug:slug>', views.AddRemoveFavorite.as_view(), name='add_remove_favorite'),
    path('cart-delete-item/<str:unique_id>', cart_views.CartDeleteItem.as_view(), name='cart_delete_item'),

]
urlpatterns += [
    path('product-add-comment/<slug:slug>', comment_views.ProductAddComment.as_view(), name='product_add_comment'),
    path('product-remove-comment/<int:id>', comment_views.ProductRemoveComment.as_view(),
         name='product_remove_comment'),
    path('comment-like/<int:id>', comment_views.CommentLikeView.as_view(), ),
    path('comment-dislike/<int:id>', comment_views.CommentDislikeView.as_view(), ),
]
