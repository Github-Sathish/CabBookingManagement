from django.contrib import admin
# Register your models here.
from cabmanagement.models import UserInfo,Booking,Cab

admin.site.register(UserInfo)
admin.site.register(Booking)
admin.site.register(Cab)
