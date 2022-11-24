
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from account.models import Place

from admins.views import admin_logout
from home.models import Category

from .models import Menu, Old_cart, Old_cart_item, Order, Restaurant_offers, Restaurants

# Create your views here.

def res_reg(request):
    place = Place.objects.all().order_by('name')
    return render(request,'restaurant_reg.html',{'place':place})

def res_home(request):
        if request.user.is_authenticated and not request.user.restaurants.is_user: 
            # details = Menu.objects.all()
            if 'n' in request.POST:
                n = request.POST['n']
                details = Menu.objects.filter(item_name__icontains=n).filter(restaurant_id = request.user.restaurants.id)
            
            else:
                details = Menu.objects.filter(restaurant_id = request.user.restaurants.id).order_by('item_name')
            count = Menu.objects.filter(restaurant_id = request.user.restaurants.id).count()
            return render(request,'restaurant_home.html',{'details':details,'count':count})
        elif request.method=="GET":
            # messages.info(request, 'invalidadted credentials')
            return redirect(res_log)
        else:
            messages.info(request, 'invalid credentials')
            return redirect(res_log)
        messages.info(request,"Account Doesn't match any restaurants Please Sign in in user section")
        return redirect(res_logout)

def res_log(request):
    return render(request,'store_login.html')

def res_login(request):
    if request.user.is_authenticated:
        return redirect(res_home)
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect(res_home)
        else:
            messages.info(request, 'invalid credentials')
            return redirect('res_log')
    else:
        messages.info(request, 'invalid credentials')
        return redirect(res_log)
    
def res_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        place1 = request.POST['place']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if len(request.FILES) != 0:
            image= request.FILES['image']
        first_name= request.POST['name']
        last_name=request.POST['name']
        rating = 0
        is_approved = False
        email = request.POST['email']
        place = Place.objects.get(id=place1)
        category = request.POST['category']
        
        if password1 == password2:
            if Restaurants.objects.filter(email=email).exists():
                messages.info(request,'Email is Taken')
                return redirect('res_reg')
            elif Restaurants.objects.filter(email=email).exists():
                messages.info("The email is already exists..")
                return redirect('res_reg')
            else:
                user = User.objects.create_user(username=email, password = password1, email=email, first_name=first_name, last_name=last_name,is_superuser=False)
                user.save()
                res_user = Restaurants.objects.create(name=name, password=password1,image=image, place=place, email=email, category=category, rating=rating,is_approved=is_approved,user_res=user)
                res_user.save()
                return redirect(res_home)
        else:
            messages.info(request,"The passwords are not matching..")
            return redirect('res_log')
        return redirect('/')
        
    else:
        return render(request, 'res_home')
    
def res_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect(res_log)

def res_ins(request):
    if request.user.is_authenticated:
        details = Restaurants.objects.all()
        category = Category.objects.all()
        return render(request, 'menu_reg.html',{'details':details,'category':category})
    return redirect(res_log)

def menu_reg(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            item_name = request.POST['name']
            item_category = request.POST['item_category']
            # item_sub_cat = request.POST['item_sub_cat']
            item_sub_cat = "Burger"
            price = request.POST['price']
            restaurant = request.POST['id']
            image = request.FILES['image']
            cat_id = request.POST['cat']
            

            category = Category.objects.get(id=cat_id)            
            res = Restaurants.objects.get(id=restaurant)
            
            menu = Menu.objects.create(item_name=item_name, item_category=item_category,item_sub_category=item_sub_cat,item_image=image,price=price,food_category=category,restaurant=res)
            menu.save()
            messages.info(request,"Menu Added Sucessfully")
            
            return redirect(res_home)
        
def res_edit(request,id):
    if request.user.is_authenticated:
        menu = Menu.objects.get(id=id)
        return render(request, 'res_menu_edit.html',{'menu':menu})
    return redirect(res_home)

def res_user_edit(request):
    if request.user.is_authenticated:
        res = Restaurants.objects.get(user_res=request.user.id)
        places = Place.objects.all()
        user =User.objects.get(id=request.user.id)
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            place1 = request.POST['place']
            place = Place.objects.get(id=place1)
            cat = request.POST['cat']
            image = request.FILES.get('image',res.image)
            
            res.name = name
            res.email = email
            res.place = place
            res.category = cat
            res.image = image
            res.save()
            
            user.username = email
            user.save()
            
            messages.info(request,"Profile Edited Sucessfully")
            return redirect(res_home)
            
        return render(request, 'restaurant_edit.html',{'res':res,'place':places})
def res_update(request,id):
    if request.method == 'POST':
        user = Menu.objects.get(id=id)
        item_name = request.POST['name']
        item_category = request.POST['item_category']
        item_sub_cat = request.POST['item_sub_cat']
        price = request.POST['price']
        image = request.FILES.get('image')
        
        try:
            if len(image) == 0:
                image = user.item_image
        except:
            image = user.item_image
        else:
            pass
            
        
        user.item_name = item_name
        user.item_category = item_category
        user.item_sub_category = item_sub_cat
        user.price = price
        user.item_image = image
        user.save()
        messages.info(request,"The Item updated sucessfully..")
        return redirect(res_home)
        
def res_delete(request,id):
   user_del = Menu.objects.get(id=id)
   user_del.delete()
   return redirect(res_home)
            

def res_available(request,id):
    item = Menu.objects.get(id=id)
    item.is_available = True
    item.save()
    return redirect(res_home)

def res_unavailable(request,id):
    item = Menu.objects.get(id=id)
    item.is_available = False
    item.save()
    return redirect(res_home)

def res_cat_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cat_name = request.POST['cat_name']
            cat_name1 = cat_name[:-1]
            if Category.objects.filter(cat_name__icontains=cat_name):
                messages.error(request,"The Category already Exists")
                return redirect(res_cat_add)
            elif Category.objects.filter(cat_name__icontains=cat_name1).exists():
                messages.error(request,"The Category already Exists")
                return redirect(res_cat_add)
            cat = Category.objects.create(cat_name=cat_name)
            cat.save()
            messages.success(request,"New Category Added")
            return redirect(res_cat_add)
        return render(request,'restaurant_cat_add.html')
    
def res_order(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(restaurant_id= request.user.restaurants.id).order_by('id')
        cart_item = Old_cart_item.objects.all()
        return render(request,"restaurant_order.html",{"order":order,'cart_item':cart_item})
    
def res_prepred(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        order.is_prepared = True
        order.save()
        return redirect(res_order)
    
def res_not_prepred(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        order.is_prepared = False
        order.save()
        return redirect(res_order)
    
def res_delivery_stat(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        stat = request.POST['stat']
        order.delivery_stat = stat
        order.save()
        return redirect(res_order)
    
def res_offers(request):
    if request.method == 'POST':
        name = request.POST['name']
        percentage = request.POST['percentage']
        restaurant = Restaurants.objects.get(id=request.user.restaurants.id)
        print (restaurant)
        max_amount = request.POST['max_amount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        offer = Restaurant_offers.objects.create(offer_name=name,restaurant=restaurant,
                                               offer_percentage=percentage,offer_max_amount=max_amount,
                                               start_date=start_date,end_date=end_date)
        offer.save()
    offers = Restaurant_offers.objects.all()
    return render(request,'restaurant_offers.html',{'offers':offers})

def res_offer_block(request,id):
    offer = Restaurant_offers.objects.get(id=id)
    offer.is_active=False
    offer.save()
    return redirect(res_offers)

def res_offer_unblock(request,id):
    offer = Restaurant_offers.objects.get(id=id)
    offer.is_active=True
    offer.save()
    return redirect(res_offers)
