
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.res_home, name='res_home'),
    path('res_reg',views.res_reg,name='res_reg'),
    path('res_log',views.res_log,name='res_log'),
    path('res_register',views.res_register,name='res_register'),
    path('res_login',views.res_login,name='res_login'),
    path('res_logout',views.res_logout,name='res_logout'),
    path('res_ins',views.res_ins,name='res_ins'),
    path('menu_reg',views.menu_reg,name='menu_reg'),
    path('delete/<int:id>',views.res_delete,name="res_delete"),
    path('edit/<int:id>',views.res_edit,name='res_edit'),
    path('update/<int:id>',views.res_update,name='res_update'),
    path('available/<int:id>',views.res_available,name='res_available'),
    path('unavailable/<int:id>',views.res_unavailable,name='res_unavailable'),
    path('res_edit',views.res_user_edit,name='res_edit'),
    path('res_cat_add',views.res_cat_add,name='res_cat_add'),
    path('res_order',views.res_order,name='res_order'),
    path('prepared/<int:id>',views.res_prepred,name='res_prepared'),
    path('not_prepared/<int:id>',views.res_not_prepred,name='res_not_prepared'),
    path('res_delivery_stat/<int:id>',views.res_delivery_stat,name='res_delivery_stat'),
    path("res_offers",views.res_offers,name='res_offers'),
    path('res_offer_block',views.res_offer_block,name='res_offer_block'),
    path('res_offer_unblock',views.res_offer_unblock,name='res_offer_unblock'),
]
    