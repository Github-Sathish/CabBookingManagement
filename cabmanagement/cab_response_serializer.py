from rest_framework import serializers

from . models import *
from userauthentication.models import *
   
class UserInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_driver = serializers.SerializerMethodField()
    is_customer = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_employee = serializers.SerializerMethodField()
    otp = serializers.SerializerMethodField()
    class Meta:
        model = UserInfo
        fields = ['is_customer','is_driver','is_available','is_admin','is_employee','otp','first_name' , 'last_name' , 'email' , 'username','license_number' , 'contact_number' , 'address' , 'age' , 'photo']
    def get_first_name(self , obj):
        return obj.user.first_name
    def get_last_name(self , obj):
        return obj.user.last_name
    def get_email(self , obj):
        return obj.user.email
    def get_username(self , obj):
        return obj.user.username
    def get_is_driver(self,obj):
        return obj.userInfoAuthentication.is_driver
    def get_is_customer(self,obj):
         return obj.userInfoAuthentication.is_customer
    def get_is_admin(self,obj):
        return obj.userInfoAuthentication.is_admin
    def get_is_employee(self,obj):
        return obj.userInfoAuthentication.is_employee
    def get_otp(self,obj):
        return obj.userInfoAuthentication.otp
    


class UserGetSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_driver = serializers.SerializerMethodField()
    is_customer = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_employee = serializers.SerializerMethodField()
    otp = serializers.SerializerMethodField()
    class Meta:
        model = UserInfo
        fields = ['is_customer','is_driver','is_available','is_admin','is_employee','otp','first_name' , 'last_name' , 'email' , 'username','license_number' , 'contact_number' , 'address' , 'photo' , 'age']
    def get_first_name(self , obj):
        return obj.user.first_name
    def get_last_name(self , obj):
        return obj.user.last_name
    def get_email(self , obj):
        return obj.user.email
    def get_username(self , obj):
        return obj.user.username
    def get_is_driver(self,obj):
        return obj.userInfoAuthentication.is_driver
    def get_is_customer(self,obj):
        return obj.userInfoAuthentication.is_customer
    def get_is_admin(self,obj):
        return obj.userInfoAuthentication.is_admin
    def get_is_employee(self,obj):
        return obj.userInfoAuthentication.is_employee
    def get_otp(self,obj):
        return obj.userInfoAuthentication.otp
    

class CabSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = Cab
        fields = ['make' , 'model' ,'year','capacity', 'registration_number' , 'user_details']
    def get_user_details(self,obj):
        #returning multiple values to the 'driver_details' in the fields by using '{}'
        return {'address' : obj.user.user.first_name ,'age' : obj.user.age}
        
class CabDetailsSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = Cab
        fields = ['make' , 'model' , 'year' , 'registration_number' , 'capacity' , 'user_details']
    def get_user_details(self , obj):
        return {'first_name' : obj.user.user.first_name , 'last_name' : obj.user.user.last_name , 'username' : obj.user.user.username}
    

class BookingSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    cab_details = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['start_location' , 'end_location' , 'user_details' , 'cab_details']
        
    def get_user_details(self,obj):
        return obj.user.user.first_name
    def get_cab_details(self,obj):
        return obj.cab.model

class BookingDetailsSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    cab_details = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['date_booked' , 'start_location' , 'end_location' , 'start_time' , 'end_time' , 'user_details' , 'cab_details']
    def get_user_details(self,obj):
        return obj.user.user.first_name
    def get_cab_details(self,obj):
        return obj.cab.model



# class CabSerializer(serializers.ModelSerializer):
#     driver_details = serializers.SerializerMethodField()
#     class Meta:
#         model = Cab
#         fields = ['driver_details' , 'make' , 'model']
#     def get_driver_details(self,obj):
#         #eturning multiple values to the 'driver_details' in the fields by using '{}'
#         return {'name' : obj.driver.name , 'age' : obj.driver.age}
    
# class BookingSerializer(serializers.ModelSerializer):
#     customer_name = serializers.SerializerMethodField()
#     class Meta:
#         model = Booking
#         fields = ['id' , 'start_location' , 'end_location' , 'customer_name']
        
#     def get_customer_name(self,obj):
#         return obj.customer.name
    
    
# #filter()
# class DriverSerializerFilter(serializers.ModelSerializer):
#     class Meta:
#         model = Driver
#         fields = ['name' , 'age' , 'is_available' , 'license_number' , 'photo']
        
# class CustomerSerializerFilter(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['name' , 'contact_number' , 'email' , 'address']

# class CustomerSerializerContain(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['name' , 'contact_number' , 'email' , 'address']
        
# class BookingSerializerOrder(serializers.ModelSerializer):
#     customer_name = serializers.SerializerMethodField()
#     cab_make = serializers.SerializerMethodField()
#     class Meta:
#         model = Booking
#         fields = ['start_location' , 'end_location' , 'customer_name' , 'cab_make']
        
#     def get_customer_name(self,obj):
#         return obj.customer.name
    
#     def get_cab_make(self,obj):
#         return obj.cab.make
    
    
    
# all() queries
# class DriverSerializer(serializers.ModelSerializer):
#     photo = serializers.SerializerMethodField()
#     class Meta:
#         model = Driver
#         fields = ['name' , 'photo']
#     def get_photo(self,obj):
#         return obj.photo.url
        
# class DriverPhotoSerializer(serializers.ModelSerializer):
   
#     class Meta:
#         model = Driver
#         fields = ['photo']


# class CustomerInfoSerializer(serializers.ModelSerializer):
#     first_name = serializers.SerializerMethodField()
#     last_name = serializers.SerializerMethodField()
#     email = serializers.SerializerMethodField()
#     class Meta:
#         model = UserInfo
#         fields = ['contact_number' , 'age' , 'first_name' , 'last_name' , 'email']
#     def get_first_name(self,obj):
#         return obj.user.first_name
#     def get_last_name(self , obj):
#         return obj.user.last_name
#     def get_email(self , obj):
#         return obj.user.email

# class DriverInfoSerializer(serializers.ModelSerializer):
#     first_name = serializers.SerializerMethodField()
#     last_name = serializers.SerializerMethodField()
#     email = serializers.SerializerMethodField()
#     class Meta:
#         model = UserInfo
#         fields = ['license_number','contact_number' , 'age' , 'first_name' , 'last_name' , 'email']
#     def get_first_name(self,obj):
#         return obj.user.first_name
#     def get_last_name(self , obj):
#         return obj.user.last_name
#     def get_email(self , obj):
#         return obj.user.email
