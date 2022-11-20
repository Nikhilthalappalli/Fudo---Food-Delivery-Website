
from django.contrib import admin
from unicodedata import name
from django.urls import path

from account.views import user_login

from . import views

urlpatterns = [
    path ('',views.admin_dash,name='admin_dash'),
    path ('admin_user',views.admin_user,name='admin_user'),
    path ('admin_store',views.admin_store,name="admin_store"),
    path ('admin_login',views.admin_login,name='admin_login'),
    path ('admin_log',views.admin_log,name='admin_log'),
    path ('admin_ins',views.admin_ins,name='admin_ins'),
    path ('admin_logout',views.admin_logout,name='admin_logout'),
    path ('block/<int:id>',views.admin_user_block,name='admin_user_block'),
    path ('unblock/<int:id>',views.admin_user_unblock,name='admin_user_unblock'),
    path ('delete/<int:id>',views.admin_delete,name='admin_delete'),
    path ('admin_insert',views.admin_insert,name='admin_insert'),
    path('approve/<int:id>',views.admin_approve,name='admin_approve'),
    path('disapprove/<int:id>',views.admin_disapprove,name='admin_disapprove'),
    path('category',views.admin_cat,name='admin_cat'),
    path('admin_cat_ins',views.admin_cat_ins,name='admin_cat_ins'),
    path('admin_cat_delete/<int:id>',views.admin_cat_delete,name="admin_cat_delete"),
    path('admin_order',views.admin_order,name="admin_user"),
    path('admin_add_place',views.admin_add_place,name='admin_add_place'),
    path('admin_offers',views.admin_offers,name='admin_offers'),
    path('admin_filter',views.admin_filter,name='admin_filter'),
    path('admin_coupons',views.admin_coupon,name='admin_coupon'),
    path('admin_coupon_unblock/<int:id>',views.admin_coupon_unblock,name='admin_coupon_unblock'),
    path('admin_coupon_block/<int:id>',views.admin_coupon_block,name='admin_coupon_block'),
    path('admin_offer_block/<int:id>',views.admin_offer_block,name='admin_offer_block'),
    path('admin_offer_unblock/<int:id>',views.admin_offer_unblock,name='admin_offer_unblock'),
    path('admin_offer_delete/<int:id>',views.admin_offer_delete,name='admin_offer_delete'),
    path('admin_sales_report',views.admin_sales,name='admin_sales'),
    path('admin_sales_filter',views.admin_sales_filter,name='admin_sales_filter'),
    path('admin_sales_filter_year',views.admin_sales_filter_year,name='admin_sales_filter_year'),
    path('admin_sales_filter_month',views.admin_sales_filter_month,name='admin_sales_filter_month'),
    
    
]