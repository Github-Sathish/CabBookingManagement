from rest_framework import serializers
from . models import *
from cabmanagement.models import *

class TripSerializer(serializers.ModelSerializer):    #import before using serializers
    customers_name = serializers.SerializerMethodField() 
    drivers_name = serializers.SerializerMethodField()
    class Meta:
        model = Trip
        fields  = ['total_cost','total_distance','date_started' , 'date_ended' , 'drivers_name' , 'customers_name']
    def get_customers_name(self,obj):
        return obj.user_customer_fk.user.first_name
        
    def get_drivers_name(self,obj):
        return obj.user_driver_fk.user.first_name
    
class TripDetailsSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField() 
    driver_name = serializers.SerializerMethodField()
    cab_model = serializers.SerializerMethodField()
    booking_end_location = serializers.SerializerMethodField()
    class Meta:
        model = Trip
        fields = ['date_started' , 'date_ended' , 'total_distance','total_cost' ,'is_completed', 'driver_name' , 'customer_name' , 'cab_model' , 'booking_end_location']
    def get_driver_name(self,obj):
        return obj.user_driver_fk.user.first_name
    def get_customer_name(self,obj):
        return obj.user_customer_fk.user.first_name
    def get_cab_model(self,obj):
        return obj.cab.model
    def get_booking_end_location(self,obj):
        return obj.booking.end_location
    
class ReviewSerializer(serializers.ModelSerializer):
    user_manyfield = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['customer_name', 'rating','total_cost' , 'review_text'  , 'user_manyfield']
        
    def get_user_manyfield(self,obj):
        drivers = []
        for i in obj.user_manyfield.all():
            drivers.append({"first_name": i.user.first_name , "username" : i.user.username})
        return drivers
    
    def get_total_cost(self,obj):
        return obj.trip.total_cost
    
    
class ReviewDetailsSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField() 
    user_manyfield = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['customer_name', 'rating', 'review_text','date_posted' ,'total_cost', 'user_manyfield']

    def get_total_cost(self,obj):
        return obj.trip.total_cost
    def get_user_manyfield(self,obj):
        drivers = []
        for i in obj.user_manyfield.all():
            drivers.append({"first_name" : i.user.first_name , "username" : i.user.username})
        return drivers