
from django.db import models
from django.contrib.auth.models import User, auth



# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=80,null= True)

class User_det(models.Model):
    name = models.CharField(max_length=120)
    place = models.ForeignKey(Place,null=True,on_delete = models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    image = models.ImageField(null=True,upload_to = 'user_pics')
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    is_user = models.BooleanField(default=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    phone_number = models.IntegerField()
    is_user = models.BooleanField()
    

    
    
    