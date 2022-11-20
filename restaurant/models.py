

from email.policy import default
from pyexpat import model
from unicodedata import category
from xmlrpc.client import Boolean
from django.contrib.auth.models import User, auth
from django.db import models
from account.models import Place, User_det


from home.models import Address, Category

# Create your models here.

class Restaurants(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    place = models.ForeignKey(Place,null=True,on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'restaurant_pics')
    rating = models.IntegerField()
    category = models.CharField(max_length=50)
    is_approved = models.BooleanField()
    user_res = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    is_user = models.BooleanField(default=False)
    
    
class Menu(models.Model):
    item_name = models.CharField(max_length=120)
    item_category = models.CharField(max_length=120) 
    item_sub_category = models.CharField(max_length=120)
    item_image = models.ImageField(upload_to = 'food_pics')
    price = models.FloatField(max_length=20)
    is_available = models.BooleanField(default=False)
    food_category = models.ForeignKey(Category, null=True , on_delete = models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, on_delete = models.CASCADE)
    
class Cart(models.Model):
    user = models.ForeignKey(User_det,null=True, on_delete = models.CASCADE)
    restaurant= models.ForeignKey(Restaurants,null=True,on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    coupon_discount = models.FloatField(default=0)
    
class Cart_item(models.Model):
    item = models.ForeignKey(Menu, null=True,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,null=True,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    offer_price = models.FloatField(default=0)
    
class Old_cart(models.Model):
    user = models.ForeignKey(User_det,null=True, on_delete = models.CASCADE)
    restaurant= models.ForeignKey(Restaurants,null=True,on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    
class Old_cart_item(models.Model):
    item = models.ForeignKey(Menu, null=True,on_delete=models.CASCADE)
    cart = models.ForeignKey(Old_cart,null=True,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
class Order(models.Model):
    user = models.ForeignKey(User_det,null=True, on_delete = models.CASCADE)
    restaurant= models.ForeignKey(Restaurants,null=True,on_delete=models.CASCADE)
    cart = models.ForeignKey(Old_cart,null=True,on_delete=models.CASCADE)
    payment = models.CharField(max_length=50)
    address = models.ForeignKey(Address,null=True,on_delete=models.CASCADE)
    grand_total = models.FloatField()
    status = models.BooleanField(default=True)
    is_prepared = models.BooleanField(null=True,default=False)
    created = models.DateTimeField(auto_now_add=True,null = True)
    delivery_stat = models.CharField(null=True,max_length=50,default='Confirmed')
    
class Restaurant_offers(models.Model):
    restaurant = models.ForeignKey(Restaurants,null=True,on_delete = models.CASCADE,blank = True )
    offer_name = models.CharField(max_length = 100)
    offer_percentage = models.FloatField()
    offer_max_amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
class Category_offers(models.Model):
    category = models.ForeignKey(Category,null=True,on_delete = models.CASCADE,blank = True )
    offer_name = models.CharField(max_length = 100)
    offer_percentage = models.FloatField()
    offer_max_amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
class Coupon(models.Model):
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length=40)
    max_amount = models.FloatField()
    discount_amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    
    
    

    