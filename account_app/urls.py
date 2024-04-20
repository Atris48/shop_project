from django.urls import path
from . import views

urlpatterns = [
    path('user-register', views.UserRegister.as_view(), name='user_register'),
    path('user-login', views.UserLogin.as_view(), name='user_login'),
    path('user-login-check-otp', views.LoginCheckOtp.as_view(), name='login_check_otp'),
    path('user-logout', views.UserLogout.as_view(), name='user_logout'),
    path('resend-otp-code', views.ResendLoginOtp.as_view(), name='resend_otp_code'),
]
