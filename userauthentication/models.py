from django.db import models

#importing django User table
from django.contrib.auth.models import User

import uuid

class BaseClass(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4, editable = False)
    class Meta:
        abstract = True


# Create your models here.
class UserInfoAuthentication(BaseClass):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    otp = models.IntegerField(default=1111 , blank =True , null = True)
    
    def __str__(self):
        return f'{self.id}==============={self.user.first_name}'
    