

from email import message
import json
from locale import currency
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from numpy import require
import razorpay
from django.core.paginator import Paginator
from account.models import Place, User_det
from account.views import user_login
from admins.views import admin_logout
from django.contrib.auth.models import User
from fudo.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from home.models import Address, Category
import restaurant
from restaurant.models import Cart, Cart_item, Category_offers, Coupon, Old_cart, Old_cart_item, Order, Restaurant_offers, Restaurants
from restaurant.models import Menu
from restaurant.views import res_cat_add, res_logout

# Create your views here.


def home(request):
    try:
        if request.user.is_authenticated and request.user.user_det.is_user and request.user.is_active:
            if 'n' in request.POST:
                n = request.POST['n']
                # details = Restaurants.objects.filter(name__icontains=n)
                details = Restaurants.objects.filter(place=request.user.user_det.place).filter(name__icontains=n)
            
            else:
                # details = Restaurants.objects.all()
                details = Restaurants.objects.filter(place=request.user.user_det.place)
            
            return render(request,'home.html',{'details':details})
        return render(request,'user_login.html')
    except:
        messages.info(request,"Account Doesn't match any user Please Sign in in restaurant section")
        return redirect(admin_logout)

def home_res(request):
    if request.user.is_authenticated:
        if 'n' in request.POST:
                n = request.POST['n']
                # res = Restaurants.objects.filter(place=request.user.user_det.place)
                # print(res)
                # details = Restaurants.objects.filter(name__icontains=n)
                details = Restaurants.objects.filter(place=request.user.user_det.place).filter(name__icontains=n)
        else:
                # details = Restaurants.objects.all()
                details = Restaurants.objects.filter(place=request.user.user_det.place)
                # print(res)
        # details = Restaurants.objects.all()
        return render(request,'home_restaurants.html',{'details':details})
    return render(request,'user_login.html')

def home_det(request,id):
    if request.user.is_authenticated:
        user = request.user.user_det
        try:
            cart = Cart.objects.get(user=user)
        except:
            cart = None
        res = Restaurants.objects.get(id=id)
        if 'n' in request.POST:
                n = request.POST['n']
                menus = Menu.objects.filter(item_name__icontains=n)
            
        else:
                menus = res.menu_set.all()
        try:
            res_offers = Restaurant_offers.objects.get(restaurant_id=id)
            cat_offers = Category_offers.objects.all()
            cat = Category.objects.all()
            return render(request,'restaurant_det.html',{'menus':menus,'res':res,'category':cat,'res_offers':res_offers,'cat_offers':cat_offers,'cart':cart})
        except:
            cat_offers = Category_offers.objects.all()
            # print(offers.offer_name)
            cat = Category.objects.all()
            return render(request,'restaurant_det.html',{'menus':menus,'res':res,'category':cat,'cat_offers':cat_offers,'cart':cart})

def home_cat_veg(request):
    if request.user.is_authenticated:
        cat = 'Veg'
        # cat = 'Non-Veg'
        details = Restaurants.objects.filter(category=cat)
        return render(request,'home_restaurants.html',{'details':details})
    return render(request,'user_login.html')

def home_cat_Non_veg(request):
    if request.user.is_authenticated:
        # cat = 'Veg'
        cat = 'Non-Veg'
        details = Restaurants.objects.filter(category=cat)
        return render(request,'home_restaurants.html',{'details':details})
    return render(request,'user_login.html')

def home_cat_both(request):
    if request.user.is_authenticated:
        # cat = 'Veg'
        cat = 'Veg & Non-Veg'
        details = Restaurants.objects.filter(category=cat)
        return render(request,'home_restaurants.html',{'details':details})
    return render(request,'user_login.html')

def home_cat(request,id1,id):
    if request.user.is_authenticated:
        res = Restaurants.objects.get(id=id1)
        print(res.name)
        cat = Category.objects.all()
        cate = Category.objects.get(id=id)
        # menus = res.menu_set.all()
        menu = Menu.objects.filter(food_category=cate).filter(restaurant=res)
        return render(request,'restaurant_det.html',{'menus':menu,'res':res,'category':cat})
    
        
def home_user_det(request):
    if request.user.is_authenticated:
        details = User_det.objects.get(user=request.user.id)
        # order = Order.objects.filter(user=details)
        p = Paginator(Order.objects.filter(user=details).order_by('-id'),9)
        page = request.GET.get('page')
        order = p.get_page(page)
        cart = Old_cart.objects.filter(user=details)
        cart_item = Old_cart_item.objects.all()
        return render(request,'home_user_dets.html',{'details':details,'orders':order,'cart':cart,'cart_item':cart_item})
    return render(request,'user_login.html')

def home_user_edit(request):
    if request.user.is_authenticated:
        id = request.user.user_det.id
        user = User_det.objects.get(id=id)
        places = Place.objects.all().order_by('name')
        user1 =User.objects.get(id=request.user.id)
        if request.method == "POST":
            name = request.POST['name']
            place1 = request.POST['place']
            phone = request.POST['phone']
            email = request.POST['email']
            image = request.FILES.get('image',user.image)
            print(image)
            place = Place.objects.get(id=place1)
            
            user.name = name
            user.place = place
            user.phone = phone
            user.email = email
            user.image = image
            user.save()
            
            user1.username = email
            user1.save()
            messages.info(request,"Profile updated sucessfully..")
            return redirect(home_user_det)
        return render(request,'home_user_edit.html',{'details':user,'place':places})
    
def user_change_password(request):
    if request.method == "POST":
        user = request.user
        old = request.POST['old']
        print(old)
        print(user.username)
        print(user.password)
        new = request.POST['new']
        confirm = request.POST['confirm']
        if new != confirm:
            messages.info(request,"The passowrds are not matching")
            return redirect(user_change_password)
        elif not user.check_password(old):
            messages.info(request,"Wrong Old Pasword")
            return redirect(user_change_password)
        else:
            user.set_password(new)
            user.save()
            return redirect(home_user_det)
    return render(request,'home_change_password.html')
    
def home_add_address(request):
    if request.user.is_authenticated:
        
        user = request.user.user_det
        try:
            cart = Cart.objects.get(user=user)
        except:
            cart = None
        
        try: 
            address = Address.objects.filter(user=user)
            context = {'details':user,'address':address,'cart':cart}
        except:
            context = {'details':user,'cart':cart}
        if request.method == 'POST':
            complete_add = request.POST['complete_address']
            floor = request.POST['floor']
            land_mark = request.POST['landmark']
            type = request.POST['add_type']
            
            new_add = Address.objects.create(complete_address=complete_add,floor=floor,land_mark=land_mark,type = type,user = user)
            new_add.save()
        return render(request, 'home_user_address.html',context)
    return render(request,'user_login.html')
    
def home_remove_address(request,id):
    if request.user.is_authenticated:
        add = Address.objects.get(id=id)
        add.delete()
        return redirect(home_add_address)
    
def home_user_delete(request):
    if request.user.is_authenticated:
        id = request.user.user_det.id
        id2 = request.user.id
        user = User_det.objects.get(id=id)
        user2 = User.objects.get(id=id2)
        user.delete()
        user2.delete()
        return render(request,'user_login.html')
    return redirect(user_login)
       
def home_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and 'code' in request.POST:
            print('code')
            user = request.user.user_det
            code = request.POST['code']
            print(code)
            cart = Cart.objects.get(user=user)
            address = Address.objects.filter(user=user)
            cart_item = Cart_item.objects.filter(cart=cart).order_by('-id')
            res = cart.restaurant
            total = 0
            for i in range(len(cart_item)):
                if cart.cancel != True:
                    if cart_item[i].offer_price !=0:
                        x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
                        total = int(total + x)
                    else:
                        x = int(cart_item[i].item.price)*int(cart_item[i].quantity)
                        total = int(total + x)
            delivery = 50
            grand_total = total+delivery
            coupon = Coupon.objects.get(code=code)
            if grand_total > coupon.max_amount:
                grand_total = grand_total-coupon.discount_amount

                print('1-',grand_total)
            else:
                message.info(request,'The Amount Is Not Valid For Coupon')
            print('2-',grand_total)
            cart.coupon_discount=grand_total
            context={'cart_item':cart_item,'total':total,'delivery':delivery,'grand_total':grand_total}
            return render(request,'home_cart.html',context)
        else:
            user = request.user.user_det
            try:
                cart = Cart.objects.get(user=user)
            except:
                empty = "Cart Is Empty"
                return render(request,'home_cart.html',{"emplty":empty})
            cart_item = Cart_item.objects.filter(cart=cart)
            for i in range(len(cart_item)):
                if cart_item[i].quantity<=0:
                    cart_item[i].delete()
            if len(cart_item)==0:
                empty = "Cart Is Empty"
                return render(request,'home_cart.html',{"empty":empty})
            else:
                total = 0
                for i in range(len(cart_item)):
                    if cart.cancel != True:
                        if cart_item[i].offer_price !=0:
                            x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
                            total = int(total + x)
                        else:
                            x = int(cart_item[i].item.price)*int(cart_item[i].quantity)
                            total = int(total + x)
                delivery = 50
                grand_total = int(total+delivery)
                    
                return render(request, 'home_cart.html',{'cart_item':cart_item,'total':total,'delivery':delivery,'grand_total':grand_total,'cart':cart})
            empty = "Cart Is Empty"
            return render(request,'home_cart.html',{"emplty":empty})
    return render(home)
        
    
def add_to_cart(request,id1,id):
    item = Menu.objects.get(id=id)
    user = request.user.user_det
    res = Restaurants.objects.get(id=id1)
    cat_offer = Category_offers.objects.all()
    try:
        res_offer = Restaurant_offers.objects.get(restaurant=res)
    except:
        res_offer = None
    messages.info(request,"Item Added to cart")
    if Cart.objects.filter(restaurant=res,user=user).exists():
        if Cart_item.objects.filter(item=item).exists():
            cart = Cart_item.objects.get(item=id)
            cart.quantity = cart.quantity+1
            cart.save()
            # return redirect(home_cart)
            return redirect (home_det,id=id1)
        else:
            cart = Cart.objects.get(user=user,restaurant=res)
            qty=1
            cart_item = Cart_item.objects.create(item=item,cart=cart,quantity=qty)
            cart_item.save()
            # return redirect(home_cart)
            return redirect (home_det,id=id1)
    elif Cart.objects.filter(user=user).exists():
        cart = Cart.objects.get(user=user)
        cart.delete()
        cart = Cart.objects.create(user=user,restaurant=res)
        qty=1
        cart_item = Cart_item.objects.create(item=item,cart=cart,quantity=qty)
        cart_item.offer_price = cart_item.item.price
        for offer in cat_offer:
            if cart_item.item.food_category == offer.category:
                off_price = cart_item.item.price * (offer.offer_percentage/100)
                if off_price > offer.offer_max_amount:
                    cart_item.offer_price = cart_item.item.price - offer.offer_max_amount
                else:
                    cart_item.offer_price = cart_item.item.price - off_price
        if res_offer:
            off_price = cart_item.item.price *(res_offer.offer_percentage/100)
            if off_price > res_offer.offer_max_amount:
                off_price = cart_item.item.price - res_offer.offer_max_amount
            else:
                off_price = cart_item.item.price - off_price
        if off_price > cart_item.offer_price:
            cart_item.offer_price = off_price
        cart_item.save()
        # return redirect(home_cart)
        return redirect (home_det,id=id1)
    else:
        cart = Cart.objects.create(user=user,restaurant=res)
        qty=1
        cart_item = Cart_item.objects.create(item=item,cart=cart,quantity=qty)
        for offer in cat_offer:
            if cart_item.item.food_category == offer.category:
                off_price = cart_item.item.price * (offer.offer_percentage/100)
                if off_price > offer.offer_max_amount:
                    cart_item.offer_price = cart_item.item.price - offer.offer_max_amount
                else:
                    cart_item.offer_price = cart_item.item.price - off_price
        if res_offer:
            off_price = cart_item.item.price *(res_offer.offer_percentage/100)
            if off_price > res_offer.offer_max_amount:
                off_price = cart_item.item.price - res_offer.offer_max_amount
            else:
                off_price = cart_item.item.price - off_price
        if res_offer and cat_offer:
            if off_price > cart_item.offer_price:
                cart_item.offer_price = off_price
        cart_item.save()
        # return redirect(home_cart)
        return redirect (home_det,id=id1)
       
def up_quantity(request,id):
    user = request.user.user_det
    cart1 = Cart.objects.get(user=user)
    cart = Cart_item.objects.get(id=id)
    cart.quantity = cart.quantity+1
    cart.save()
    qty = cart.quantity
    cart_item = Cart_item.objects.filter(cart=cart1)
    total = 0
    for i in range(len(cart_item)):
            x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
            total = int(total + x)
    delivery = 50
    grand_total = int(total+delivery)
    print(qty)
    print(total)
    print(grand_total)
    return JsonResponse({'qty':qty,'total':total,'grand_total':grand_total})
    # return redirect(home_cart)

def down_quantity(request,id):
    user = request.user.user_det
    cart1 = Cart.objects.get(user=user)
    cart = Cart_item.objects.get(id=id)
    cart.quantity = cart.quantity-1
    cart.save()
    qty = cart.quantity
    cart_item = Cart_item.objects.filter(cart=cart1)
    total = 0
    for i in range(len(cart_item)):
            x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
            total = int(total + x)
    delivery = 50
    grand_total = int(total+delivery)
    print(qty)
    print(total)
    print(grand_total)
    return JsonResponse({'qty':qty,'total':total,'grand_total':grand_total})
    # return redirect(home_cart)

def remove_cart(request):
    user = request.user.user_det
    cart = Cart.objects.get(user=user)
    cart.delete()
    return redirect('home')

def remove_cart_item(request,id):
    cart_item = Cart_item.objects.get(id=id)
    cart_item.delete()
    return redirect(home_cart)


client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))

def order_placed(request):
    return render(request,'home_order_placed.html')

def check_out(request):
    if request.method == "POST" and 'address' in request.POST :
        user = request.user.user_det
        cart = Cart.objects.get(user=user)
        cart_item = Cart_item.objects.filter(cart=cart)
        res = cart.restaurant
        address_id = request.POST.get('address')
        print(address_id)
        # address_id = body['address_id']
        address = Address.objects.get(id=address_id)
        payment = request.POST.get('payment')
        print(payment)
        total = 0
        for i in range(len(cart_item)):
            if cart.cancel != True:
                if cart_item[i].offer_price !=0:
                    x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
                    total = int(total + x)
                else:
                    x = int(cart_item[i].item.price)*int(cart_item[i].quantity)
                    total = int(total + x)
        delivery = 50
        grand_total = int(total+delivery)
        print(cart.coupon_discount)
        grand_total = grand_total-cart.coupon_discount
        order_amount = grand_total
        print(order_amount)
        print(grand_total)
        order_currency = 'INR'
        print("user= ",user)
        print("cart= ",cart)
        print("res= ",res)
        print("add= ",address)
        print('payment=',payment)
        old_cart = Old_cart.objects.create(user=user,restaurant=res)
        old_cart.save()
        for i in cart_item:
            print(i.item.id)
            qty =i.quantity
            print(qty)
            item = Menu.objects.get(id=i.item.id)
            print(item.item_name)
            old_cart_item = Old_cart_item.objects.create(item=item,cart=old_cart,quantity=qty)
            old_cart_item.save()
        payment_order = client.order.create(dict(amount = order_amount,currency=order_currency,payment_capture=1))
        payment_order_id = payment_order['id']
        order = Order.objects.create(user=user,restaurant=res,cart=old_cart,address=address,payment=payment,grand_total=grand_total)
        order.save()
        cart.delete()
        return render(request,'home_order_placed.html')
    elif request.method == 'POST' and 'code' in request.POST:
        print('code')
        user = request.user.user_det
        code = request.POST['code']
        print(code)
        cart = Cart.objects.get(user=user)
        address = Address.objects.filter(user=user)
        cart_item = Cart_item.objects.filter(cart=cart)
        res = cart.restaurant
        total = 0
        for i in range(len(cart_item)):
            if cart.cancel != True:
                if cart_item[i].offer_price !=0:
                    x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
                    total = int(total + x)
                else:
                    x = int(cart_item[i].item.price)*int(cart_item[i].quantity)
                    total = int(total + x)
        delivery = 50
        grand_total = total+delivery
        try:
            coupon = Coupon.objects.get(code=code)
        except:
            messages.info(request,'Invalid Code')
            context={'total':total,'delivery':delivery,'cart_item':cart_item,'grand_total':grand_total,'address':address}
            return render(request,'home_checkout.html',context)
        if coupon.is_active:
            if grand_total > coupon.max_amount:
                grand_total = float(grand_total-coupon.discount_amount)
                cart.coupon_discount=coupon.discount_amount
                cart.save()
                print(cart.coupon_discount)
                print('1-',grand_total)
            else:
                messages.info(request,'The Amount Is Not Valid For Coupon')
        else:
            messages.info(request,'The Coupon Code Is Expired')
            
        
        paypal = grand_total/80
        print(paypal,type(paypal))
        context={'total':total,'delivery':delivery,'cart_item':cart_item,'grand_total':grand_total,'address':address,'amount':paypal}
        return render(request,'home_checkout.html',context)
    else:
        user = request.user.user_det
        address = Address.objects.filter(user=user)
        try:
            cart = Cart.objects.get(user=user)
        except:
            empty = "Cart Is Empty"
            return render(request,'home_cart.html',{"emplty":empty})
        cart_item = Cart_item.objects.filter(cart=cart)
        if len(cart_item)==0:
            empty = "Cart Is Empty"
            return render(request,'home_cart.html',{"emplty":empty})
        else:
            total = 0
            for i in range(len(cart_item)):
                if cart.cancel != True:
                    if cart_item[i].offer_price !=0:
                        x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
                        total = int(total + x)
                    else:
                        x = int(cart_item[i].item.price)*int(cart_item[i].quantity)
                        total = int(total + x)
            delivery = 50
            grand_total = int(total+delivery)
            paypal = grand_total/80
        context={'total':total,'delivery':delivery,'cart_item':cart_item,'grand_total':grand_total,'address':address,'paypal':paypal}
        return render(request,'home_checkout.html',context)
def razorpay(request):
    user = request.user.user_det
    cart = Cart.objects.get(user=user)
    cart_item = Cart_item.objects.filter(cart=cart)
    total = 0
    for i in range(len(cart_item)):
        if cart.cancel != True:
            if cart_item[i].offer_price !=0:
                x = int(cart_item[i].offer_price)*int(cart_item[i].quantity)
                total = int(total + x)
            else:
                x = int(cart_item[i].item.price)*int(cart_item[i].quantity)
                total = int(total + x)
    delivery = 50
    grand_total = int(total+delivery)
    
    return JsonResponse({'total': grand_total,})
    
def home_order_tracking(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        return render(request,'home_order_tracking.html',{'order':order})
    
def home_order_cancel(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        order.status = False
        order.save()
        return redirect(home_user_det)
    
