
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('home_res',views.home_res,name='home_res'),
    path('home_cat_veg',views.home_cat_veg,name="home_cat_veg"),
    path('home_cat_Non_veg',views.home_cat_Non_veg,name="home_cat_Non_veg"),
    path('home_cat_both',views.home_cat_both,name="home_cat_both"),
    path('home_det/<int:id>',views.home_det,name="home_det"),
    path('home_user_det',views.home_user_det,name='home_user_det'),
    path('home_user_edit',views.home_user_edit,name='home_user_edit'),
    path('home_det/<int:id1>/home_cat/<int:id>',views.home_cat,name="home_cat"),
    path('address',views.home_add_address,name='home_add_address'),
    path('delete',views.home_user_delete,name="home_user_delete"),
    path('home_det/<int:id1>/home_cat_add/<int:id>',views.add_to_cart,name="home_cat_add"),
    path('user_change_password',views.user_change_password,name='user_change_password'),
    path('cart',views.home_cart,name='home_Cart'),
    path('up_quantity/<int:id>',views.up_quantity,name="up_quantity"),
    path('down_quantity/<int:id>',views.down_quantity,name="down_quantity"),
    path('remove_cart',views.remove_cart,name="remove_cart"),
    path('remove_add/<int:id>',views.home_remove_address,name='home_remove_address'),
    path('checkout',views.check_out,name="checkout"),
    path('order_track/<int:id>',views.home_order_tracking,name="home_order_tracking"),
    path('order_cancel/<int:id>',views.home_order_cancel,name='home_order_cancel'),
    path('order_placed',views.order_placed,name='order_placed'),
    path('razorpay',views.razorpay,name='razorpay'),
    path('remove_cart_item/<int:id>',views.remove_cart_item,name='remove_cart_item'),
]
    