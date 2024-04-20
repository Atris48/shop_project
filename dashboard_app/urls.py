from django.urls import path
from . import views
from . import chart_views

urlpatterns = [
    path('dashboard', views.IndexView.as_view(), name='dashboard'),
    path('chat-list', views.ChatListView.as_view(), name='chat_list'),
    path('most-sell-products', views.MostSellProduct.as_view(), name='most_sell_products'),
    path('admin-ban-user/<str:phone>', views.admin_ban_user, name='admin_ban_user'),

]

# charts

urlpatterns += [
    path('last-month-order-chart', chart_views.LastMonthOrderChart.as_view(), name='last_month_order_data'),
    path('last-week-order-chart', chart_views.LastWeekOrderChart.as_view(), name='last_week_order_data'),
    path('last-day-order-chart', chart_views.LastDayOrderChart.as_view(), name='last_day_order_data'),
    path('last-year-order-chart', chart_views.LastYearOrderChart.as_view(), name='last_year_order_data'),
    path('year-order-chart', chart_views.YearChart.as_view(), name='year_chart'),
    path('all-order-chart', chart_views.AllOrderChart.as_view(), name='all_order_data'),
    # product chart
    path('product-sell-statistics', chart_views.ProductSaleStatistics.as_view(), name='product_sell_statistics'),
    path('product-attribute-sell-statistics', chart_views.ProductAttributeSaleStatistics.as_view(),
         name='product_attribute_sell_statistics'),
    path('product-comparison-sell-chart', chart_views.ProductComparisonSellChart.as_view(),
         name='product_comparison_sell_chart'),
    # user
    path('user-signup-chart', chart_views.UserSignupChart.as_view(), name='user_signup_chart'),
]
