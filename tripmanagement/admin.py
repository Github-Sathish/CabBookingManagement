from django.contrib import admin

from tripmanagement.models import Review,Trip
# Register your models here.
admin.site.register(Trip)
admin.site.register(Review)