
from django.db import models



from account.models import User_det



# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(max_length=100)
    
class Address(models.Model):
    complete_address = models.TextField()
    floor = models.CharField(max_length=100, null=True)
    land_mark = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=50)
    user = models.ForeignKey(User_det,null=True, on_delete = models.CASCADE)


    
    