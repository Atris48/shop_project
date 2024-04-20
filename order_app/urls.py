from django.urls import path
from . import views

urlpatterns = [
    path('checkout-detail', views.FactorDetail.as_view(), name='factor_detail'),
    path('checkout-delete-item/<int:id>', views.FactorDeleteItem.as_view(), name='factor_delete_item'),
    path('checkout-delete-all-item', views.FactorDeleteAllItem.as_view(), name='factor_delete_all_item'),
    path('checkout-increase-item-quantity/<int:id>', views.FactorItemIncreaseQuantity.as_view()),
    path('checkout-decrease-item-quantity/<int:id>', views.FactorItemDecreaseQuantity.as_view()),
    path('checkout-discount/<int:id>', views.FactorDiscountView.as_view(), name='factor_discount'),
    path('checkout-address/<int:id>', views.FactorAddress.as_view(), name='factor_address'),
    path('checkout-payment/<int:id>', views.FactorPayment.as_view(), name='factor_payment'),
    path('checkout-verify-pay/<int:id>', views.FactorVerifyPay.as_view(), name='factor_verify_pay'),
]
