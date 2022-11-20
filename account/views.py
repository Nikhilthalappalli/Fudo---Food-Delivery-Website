
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from account import CustomBackend
from account.mixin import MessageHandler
from account.models import Place, User_det

# Create your views here.


def user_reg(request):
    place = Place.objects.all().order_by('name')
    return render(request, 'user_register.html',{'place':place})
def user_log(request):
    return render(request,'user_login.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('user_log')
    else:
        return render(request,"user_login.html")

def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['name']
        email = request.POST['email']
        place1 = request.POST['place']
        print(place1)
        user_image = None
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        place = Place.objects.get(id=place1)
        
        if len(phone) <=10 and len(phone) >= 13:
            messages.info(request,'Phone is not valid')
            return redirect('user_register')
        
        if password1 == password2:
            if User_det.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exits')
                return redirect('user_register')
            elif User_det.objects.filter(phone=phone).exists():
                messages.info("The Number already exists..")
                return redirect('user_register')
            else:
                otp=1
                message_handler = MessageHandler(phone,otp).sent_otp_on_phone()
                context = {'email':email,'first_name':first_name,'last_name':last_name,'place':place1,'user_image':user_image,
                           'password1':password1,'phone':phone}
                return render(request,'signup_otp.html',context)
                
        else:
            messages.info(request,"The passwords are not matching..")
            return redirect('user_register')
        return redirect('/')
        
    else:
        return render(request, 'user_register.html')
    
def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

# def check(request):
#     dests = Destination.objects.all()
#     if request.user.is_authenticated:
#         return render(request, 'home.html',{'dests':dests})
#     return redirect('user_login')



def number_check(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST' and request.POST['phone_number']:
        # global phone
        phone=request.POST['phone_number']
        print("phone1=",phone)
        otp=1
        message_handler = MessageHandler(phone,otp).sent_otp_on_phone()
        return render(request,'otp_validation.html',{'phone':phone})
    return render(request,'otp_login.html')
    

def otp_validate(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST' and request.POST['otp']:
        otp1= request.POST.get('otp')
        phone = request.POST.get('phone')
        validate = MessageHandler(phone,otp1).validate()
        print("validate=",validate)
        if validate=="approved":
            user=CustomBackend.CustomBackend.authenticate(request,phone_number=phone)
            print("-----")
            print (user)
            
            return redirect('home')
        
    return render(request,'otp_validation.html')

def otp_validate_reg(request):
    if request.method=='POST' and request.POST['otp']:
        otp1= request.POST.get('otp')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        user_image = request.POST.get('user_image')
        place1 = request.POST.get('place')
        place = Place.objects.get(id=place1)
        phone = request.POST.get('phone')
        print(otp1,email,first_name,last_name,password1,place,phone,user_image)
        validate = MessageHandler(phone,otp1).validate()
        print("validate=",validate)
        if validate=="approved":
            user = User.objects.create_user(username=email,
                                            password = password1,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name)
            user.save()
            acc_user = User_det.objects.create(name=first_name, place = place, email=email,phone=phone,user=user)
            acc_user.save()
            auth.login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        messages.info(request,"Enter Valid OTP")
    messages.info(request,"Enter Valid OTP")
    return render(request,'signup_otp.html')

