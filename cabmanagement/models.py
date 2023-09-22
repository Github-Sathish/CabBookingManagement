#customer - driver assign user 
#do validation email,phone no. exist already 
#add , edit


from django.db import models
import uuid

from django.contrib.auth.models import User

#importing UserInfoAuthentication from userauthentication app
from userauthentication.models import UserInfoAuthentication


class BaseClass(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4, editable = False)
    class Meta:
        abstract = True

#merging Driver and Customer
class UserInfo(BaseClass):
    user = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank= True)
    userInfoAuthentication = models.ForeignKey(UserInfoAuthentication , on_delete=models.CASCADE , blank = True , null=True)
    license_number = models.CharField(max_length=255,blank=True , null = True)
    contact_number = models.IntegerField(blank = True , null = True)
    address = models.CharField(max_length=255,blank=True , null = True)
    photo = models.ImageField(blank=True , null=True)
    age = models.IntegerField(blank =  True , null = True)
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.id}============={self.user}'


    
class Cab(BaseClass):
    make = models.CharField(max_length=200,null=True,blank=True)
    model = models.CharField(max_length=200,null=True,blank=True)   
    year = models.IntegerField(default=None)                        #year is none 
    registration_number = models.CharField(max_length=200,null=True,blank=True)
    capacity = models.IntegerField(default=0)
    user = models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True,blank=True)  #User

    def __str__(self):
        return f'{self.id}==={self.model}'
      
class Booking(BaseClass):
    date_booked = models.DateTimeField(null=True,blank=True)
    start_location = models.CharField(max_length=200,null=True,blank=True)
    end_location = models.CharField(max_length=200,null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    #user == customer since customer going to booking
    user = models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True,blank=True)
    cab = models.ForeignKey(Cab,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return f"{self.id}==={self.user.user.first_name}========={self.cab.user.user.first_name}"
    
    
    
    

# class Driver(BaseClass):
#     user = models.ForeignKey(User,on_delete=models.SET_NULL , null = True , blank=True)
#     #
#     #name = models.CharField(max_length=100,null=True,blank=True)
#     #email = models.EmailField(max_length=250,null=True,blank=True)
#     contact_number = models.CharField(max_length=10,null=True,blank=True)
#     license_number = models.CharField(max_length=100,null=True,blank=True)
#     is_available = models.BooleanField(default=True)
#     photo = models.ImageField(upload_to='driver_img',blank=True)
#     age = models.IntegerField(default = 18 , blank = True , null = True)

#     def __str__(self):
#         return str(self.id)+"==="

    
# class Customer(BaseClass):
#     # name = models.CharField(max_length=200,blank=True,null=True)
#     user = models.ForeignKey(User , on_delete = models.SET_NULL , null = True , blank = True)
    
#     contact_number = models.CharField(max_length=10,blank=True,null=True)
#     # email = models.EmailField(max_length=100,null=True,blank=True)
#     address = models.TextField(null=True,blank=True)

#     def __str__(self):
#         return str(self.id)+"==="
 