from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth,User
from django.shortcuts import redirect

from account.models import User_det
# from account.views import user_reg

# User = get_user_model()

class CustomBackend(BaseBackend):
   def authenticate(request, phone_number):
       # Check the token and return a user.
       try:
        #    phone_number=phone_number[3:]
           print(phone_number)
           user1 = User_det.objects.get(phone=phone_number)
           user = User.objects.get(id=user1.user_id)
           auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')

       except user.DoesNotExist:
           return None
       
# def user_create(request,email,username,password,phone):
#     try:
#         user_name = user_name
#         password = password
#         user = User.objects.create(username=user_name,password=password)
#         user.save()
#     except:
#         return redirect(user_reg)
