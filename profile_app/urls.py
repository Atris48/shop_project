from django.urls import path
from . import views

urlpatterns = [
    path('profile-desktop-menu/<str:phone>', views.profile_desktop_menu, name='profile_desktop_menu'),
    path('profile-mobile-menu/<str:phone>', views.profile_mobile_menu, name='profile_mobile_menu'),
    path('profile-mobile-header-menu/<str:phone>', views.profile_mobile_header_menu, name='profile_mobile_header_menu'),
    path('user-edit-profile/<str:phone>', views.UserEditProfile.as_view(), name='user_edit_profile'),
    path('user-change-password/<str:phone>', views.UserChangePassword.as_view(), name='user_change_password'),
    path('user-profile-dashborad/<str:phone>', views.UserProfileDashboard.as_view(), name='user_profile_dashboard'),
    path('user-profile-favorites/<str:phone>', views.UserProfileFavorite.as_view(), name='user_profile_favorites'),
    path('user-profile-orders/<str:phone>', views.UserProfileOrders.as_view(), name='user_profile_orders'),
    path('user-profile-order-detail/<str:unique_id>', views.UserProfileOrderDetail.as_view(),
         name='user_profile_order_detail'),
    path('user-profile-order-referral/<str:unique_id>', views.ReferralOrder.as_view(),
         name='user_profile_order_referral'),
    path('user-profile-notifications/<str:phone>', views.UserProfileNotification.as_view(),
         name='user_profile_notifications'),
    path('user-profile-prices/<str:phone>', views.UseGetPrize.as_view(),
         name='user_profile_prizes'),
    path('user-profile-address/<str:phone>', views.UserProfileAddress.as_view(), name='user_profile_address'),
    path('user-profile-add-address/<str:phone>', views.AddAddress.as_view(), name='user_profile_add_address'),
    path('user-profile-delete-address/<int:id>', views.DeleteAddress.as_view(), name='user_profile_delete_address'),
]
