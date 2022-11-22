
import re
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from numpy import require
import razorpay

from home.models import Category

import restaurant
from restaurant.models import Category_offers, Coupon, Menu, Old_cart_item, Order, Restaurants
from account.models import Place, User_det
from django.core.paginator import Paginator

# @never_cache
def admin_log(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin_user)
    return render(request,'admin_login.html')

def admin_ins(request):
    if request.user.is_authenticated or request.user.is_superuser:
        return render(request, 'admin_insert.html')
    return redirect(admin_user)


def admin_dash(request):
    if request.user.is_authenticated:
        user_count = User_det.objects.all().count()
        res_count = Restaurants.objects.all().count()
        app_count = Restaurants.objects.filter(is_approved=True).count()
        restaurant = Restaurants.objects.all()
        cart_item = Old_cart_item.objects.all()
        res = Restaurants.objects.all()
        a=[]
        for i in res:
            x = Menu.objects.filter(restaurant=i).count()
            a.append(x)
        cat = Category.objects.all()
        order = Order.objects.all().order_by('id')
        paypal = Order.objects.filter(payment='PayPal').count()
        razorpay = Order.objects.filter(payment='Razorpay').count()
        cash = Order.objects.filter(payment='Cash On Delivery').count()
        context = {'cat':cat,'user_count':user_count,'res_count':res_count,
                   'app_count':app_count,'restaurant':restaurant,
                   'order':order,'cart_item':cart_item,
                   'paypal':paypal,'razorpay':razorpay,'cash':cash,
                   'res':res,'a':a}
        return render(request,'admin_dashboard.html',context)
    return redirect(admin_log)


@never_cache
def admin_user(request):
    if request.user.is_authenticated:
        # if 'n' in request.POST:
        #     n = request.POST['n']
        #     details = User_det.objects.filter(name__icontains=n)
        #     details1 = User.objects.filter(first_name__icontains=n)
        # else:
            
        details1 = User.objects.all()
        details = User_det.objects.all()
        # p = Paginator(User.objects.all(),4)
        # page = request.GET.get('page')
        # details1 = p.get_page(page)
        count = User_det.objects.all().count()
        
        # act_count = User_det.objects.filter(is_active=True).count()
        # sup_count = User_det.objects.filter(is_superuser=True).count()
        context = {'details':details,'count':count,'details1':details1}
        return render(request,'admin_home.html',context)
    return redirect(admin_log)

@never_cache
def admin_store(request):
    if request.user.is_authenticated:
        if 'n' in request.POST:
            n = request.POST['n']
            details = User.objects.filter(first_name__icontains=n)
            
        else:
            details = User.objects.all()
            
        count = Restaurants.objects.all().count()
        
        # act_count = User_det.objects.filter(is_active=True).count()
        # sup_count = User_det.objects.filter(is_superuser=True).count()
        context = {'details':details,'count':count}
        return render(request,'admin_stores.html',context)
    return redirect(admin_log)


@never_cache
def admin_login(request):
    if request.user.is_authenticated or request.user.is_superuser:
        return redirect(admin_dash)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None and user.is_superuser:
            # auth.login(request, user)
            auth.login(request, user)
            return redirect(admin_dash)
        else:
            messages.info(request, 'Credentials does not match with admin user')
            return redirect(admin_log)
    else:
        return render(request,"admin_login.html")
    
    
@never_cache   
def admin_logout(request):
    if request.user.is_authenticated or request.user.is_superuser:
        auth.logout(request)
    return redirect('/')

def admin_insert(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        adm = request.POST.get('adm')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is alreadey Taken')
                return redirect('admin_ins')
            elif User.objects.filter(email=email).exists():
                messages.info("The email is already exists..")
                return redirect('admin_ins')
            else:
                user = User.objects.create_user(username=username, password = password1, email=email, first_name=first_name, last_name=last_name,is_superuser=adm)
                user.save()
                return redirect(admin_dash)
        else:
            messages.info(request,"The passwords are not matching..")
            return redirect('admin_ins')
        return redirect('/')
        
    else:
        return redirect('admin_insert')
# @never_cache
def admin_edit(request,id):
    if request.user.is_authenticated or request.user.is_superuser:
        user_details = User.objects.all()
        user = Restaurants.objects.get(id=id)
        return render(request, 'admin_edit.html',{'user_details':user})
    return redirect(admin_store)

def admin_user_block(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=id)
        print(user.is_active)
        user.is_active = False
        user.save()
    return redirect(admin_dash)
        
        
def admin_user_unblock(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=id)
        print(user)
        user.is_active = True
        user.save()
    return redirect(admin_dash)

def admin_approve(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        res = Restaurants.objects.get(id=id)
        res.is_approved=True
        res.save()
        return redirect(admin_store)

def admin_disapprove(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        res = Restaurants.objects.get(id=id)
        res.is_approved=False
        res.save()
        return redirect(admin_store)
    
def admin_cat(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        return render(request,'admin_cat_manage.html',{'category':category})
    return render(request,'admin_login.html')
    
def admin_cat_ins(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cat_name = request.POST['cat_name']
            cat_name1 = cat_name[:-1]
            if Category.objects.filter(cat_name__icontains=cat_name):
                messages.info(request,"The Category already Exists")
                return redirect(admin_cat)
            elif Category.objects.filter(cat_name__icontains=cat_name1).exists():
                messages.info(request,"The Category already Exists")
                return redirect(admin_cat)
            cat = Category.objects.create(cat_name=cat_name)
            cat.save()
            return redirect(admin_cat)
        return render(request,'admin_cat_ins.html')
    
def admin_cat_delete(request,id):
    if request.user.is_authenticated:
        cat = Category.objects.get(id=id)
        cat.delete()
        return redirect(admin_cat)
        
        
def admin_order(request):
    if request.user.is_authenticated:
        order = Order.objects.all().order_by('-id')
        # p = Paginator(Order.objects.all(),6)
        # page = request.GET.get('page')
        # order = p.get_page(page)
        return render(request,"admin_order.html",{"order":order})
    
def admin_sales(request):
    if request.user.is_authenticated:
        sales = Order.objects.all()
        return render(request,"admin_sales_report.html",{"sales":sales})

def admin_delete(request,id):
   user_del = User.objects.get(id=id)
   user_del.delete()
   user = User.objects.all()
   return redirect(admin_user)

def admin_add_place(request):
    if request.method=="POST":
        input = request.POST['input']
        print(input)
        if Place.objects.filter(name=input).exists():
            messages.info(request,"The Place Already Exists")
            return redirect(admin_dash)
        place = Place.objects.create(name=input)
        place.save()
        messages.info(request,"Place Added Sucessfully")
    return redirect(admin_dash)

def admin_offers(request):
    if request.method == "POST":    
        name = request.POST['name']
        percentage = request.POST['percentage']
        id = request.POST['category']
        category = Category.objects.get(id=id)
        max_amount = request.POST['max_amount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if Category_offers.objects.filter(category=category).exists():
            messages.info(request,"Offer On This Category Already Exists")
            cat = Category.objects.all()
            offers = Category_offers.objects.all()
            return render(request,'admin_offers.html',{'cat':cat,'offers':offers})
        offer = Category_offers.objects.create(offer_name=name,category=category,
                                               offer_percentage=percentage,offer_max_amount=max_amount,
                                               start_date=start_date,end_date=end_date)
        offer.save()
    cat = Category.objects.all()
    offers = Category_offers.objects.all()
    return render(request,'admin_offers.html',{'cat':cat,'offers':offers})

def admin_filter(request):
    print(request.method)
    start = request.POST['start_date']
    end = request.POST['end_date']
    print("end=",end)
    order = Order.objects.filter(created__range=[start,end])
    print(order)
    n=len(order)
    return render(request,"admin_order.html",{"order":order})

def admin_coupon(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        max_amount = request.POST['max_amount']
        discount_amount = request.POST['discount_amount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        coupon = Coupon.objects.create(name=name,code=code,max_amount=max_amount,
                                       discount_amount=discount_amount,start_date=start_date
                                       ,end_date=end_date)
        coupon.save()
    coupons = Coupon.objects.all()
    return render(request,'admin_coupons.html',{'coupons':coupons})

def admin_coupon_block(request,id):
    coupon = Coupon.objects.get(id=id)
    coupon.is_active= False
    coupon.save()
    return redirect(admin_coupon)

def admin_coupon_unblock(request,id):
    coupon = Coupon.objects.get(id=id)
    coupon.is_active= True
    coupon.save()
    return redirect(admin_coupon)

def admin_coupon_delete(request,id):
    offer = Coupon.objects.get(id=id)
    offer.delete()
    return redirect(admin_coupon)

def admin_coupon_edit(request,id):
    coupon = Coupon.objects.get(id=id)
    name = request.POST['name']
    code = request.POST['code']
    max_amount = request.POST['max_amount']
    discount_amount = request.POST['discount_amount']
    # start_date = request.POST['start_date']
    # end_date = request.POST['end_date']
    
    coupon.name = name
    coupon.code = code
    coupon.max_amount = max_amount
    coupon.discount_amount = discount_amount
    # coupon.start_date = start_date
    # coupon.end_date  = end_date
    coupon.save()
    
    return redirect(admin_coupon)

def admin_offer_block(request,id):
    offer = Category_offers.objects.get(id=id)
    offer.is_active=False
    offer.save()
    return redirect(admin_offers)

def admin_offer_unblock(request,id):
    offer = Category_offers.objects.get(id=id)
    offer.is_active=True
    offer.save()
    return redirect(admin_offers)

def admin_offer_delete(request,id):
    offer = Category_offers.objects.get(id=id)
    offer.delete()
    return redirect(admin_offers)



def admin_sales_filter(request):
    print(request.method)
    start = request.POST['start_date']
    end = request.POST['end_date']
    print("end=",end)
    order = Order.objects.filter(created__range=[start,end])
    print(order)
    n=len(order)
    return render(request,"admin_sales_report.html",{"order":order})

def admin_sales_filter_year(request):
    date = request.POST['date']
    sales = Order.objects.filter(created__year=date)
    return render(request,"admin_sales_report.html",{"sales":sales})

def admin_sales_filter_month(request):
    date = request.POST['date']
    sales = Order.objects.filter(created__month=date)
    return render(request,"admin_sales_report.html",{"sales":sales})