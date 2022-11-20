
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('user_register',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_log',views.user_log,name='user_log'),
    path('user_reg',views.user_reg,name='user_reg'),
    path('user_logout',views.user_logout,name="user_logout"),
    path('number_check',views.number_check,name="number_check"),
    path('otp_validate',views.otp_validate,name="otp_validation"),
    path('otp_validation_reg',views.otp_validate_reg,name="'otp_validation_reg"),
]
    