from django.db import models
from cabmanagement.models import Cab,Booking,BaseClass

#importing django user table
from django.contrib.auth.models import User

from cabmanagement.models import *

class Trip(BaseClass):
    date_started = models.DateField(null= True,blank=True)
    date_ended = models.DateField(null= True,blank=True)
    total_distance = models.IntegerField(default=0,null=True,blank=True)
    total_cost = models.IntegerField(default=0,null=True,blank=True)
    is_completed = models.BooleanField(default=True)
    user_driver_fk = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True,null=True , related_name='driver')
    user_customer_fk = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True,null=True , related_name='customer')
    cab = models.ForeignKey(Cab,on_delete=models.SET_NULL,blank=True,null=True)
    booking = models.ForeignKey(Booking,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return f'{self.id}========={self.user_driver_fk.user.first_name}======={self.user_customer_fk.user.first_name}'
    
class Review(BaseClass):
    customer_name = models.CharField(max_length=200,blank=True,null=True)
    review_text = models.TextField(null=True,blank=True)
    rating = models.IntegerField(default=1,null=True,blank=True)
    date_posted = models.DateField(null=True,blank=True)
    trip = models.ForeignKey(Trip,on_delete=models.SET_NULL , null=True,blank=True)
    user_manyfield = models.ManyToManyField(UserInfo)   #User == Driver #changed to User== UserInfo

    def __str__(self):
        return f"{self.customer_name}======={self.id}"

