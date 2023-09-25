from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from . models import UserInfo  #Driver
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from . cab_response_serializer import *

from .cab_request_serializer import *

#for image
from django.core.files.base import ContentFile
import base64
import random

#for authentication
from rest_framework import authentication , permissions

#for automatci token creation
from userauthentication.utils import *

    
class AddUserInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        data = request.data
        #validation
        validation = UserInfoValidationSerializer(data = request.data)
        if validation.is_valid():
            if 'id' not in data:
                if User.objects.filter(email = data['user']['email']).count() == 0:
                    userinfo_form = {}
                    userinfo_form['contact_number'] = data['contact_number']
                    #'if' because customer dont have license number
                    if 'license_number' in data:
                        userinfo_form['license_number'] = data['license_number']
                    userinfo_form['age'] = data['age']
                    userinfo_form['address'] = data['address']
                    userinfo_form['is_available'] = data['is_available']
                    

                    #this is one method when the adding has foreign key another on cab
                    user_form = {}
                    user_form['first_name'] = data['user']['first_name']
                    user_form['last_name'] = data['user']['last_name']
                    user_form['email'] = data['user']['email']
                    user_form['username'] = data['user']['email']
                    user_form['password'] = data['user']['password']
                    user = User.objects.create(**user_form)
                    
                    #automatically creating new token per user
                    token = get_token_by_user(user)
                    
                    userInfoAuthentication_form = {}
                    userInfoAuthentication_form['is_customer'] = data['userInfoAuthentication']['is_customer']
                    userInfoAuthentication_form['is_driver'] = data['userInfoAuthentication']['is_driver']
                    userInfoAuthentication_form['is_employee'] = data['userInfoAuthentication']['is_employee']
                    userInfoAuthentication_form['otp'] = data['userInfoAuthentication']['otp']
                    userInfoAuthentication_form['is_admin'] = data['userInfoAuthentication']['is_admin']
                    
                    userInfoAuthentication = UserInfoAuthentication.objects.create(**userInfoAuthentication_form , user = user)
                    
                    #photo
                    #driver_form['photo'] = data['s']
                    if 'photo' in data: 
                        image_data = ContentFile(base64.b64decode(data['photo']))
                        file_name = str(random.randint(11111,99999))+'.jpg'
                    userinfo = UserInfo.objects.create(**userinfo_form , user = user , userInfoAuthentication = userInfoAuthentication)  #**means it sends as keyword arguments(means key value pair)
                    userinfo.photo.save(file_name , image_data , save = True)
                    
                    #UserInfo.objects.create(**userinfo_form , user = user , userInfoAuthentication = userInfoAuthentication)
                    
                    return Response({"Message":"UserInfo form added successfully"})
                else:
                    return Response({"message" : "user(email) is already existed"})
            
            else:
                userinfo_edit_details = UserInfo.objects.get(id = data['id'])
                if 'first_name' in data['user']: 
                    userinfo_edit_details.user.first_name = data['user']['first_name']
                if 'last_name' in data['user']:
                    userinfo_edit_details.user.last_name = data['user']['last_name']
                if 'password' in data['user']:
                    userinfo_edit_details.user.password = data['user']['password']
                #username and email cant be changed

                if 'contact_number' in data:
                    userinfo_edit_details.contact_number = data['contact_number']
                if 'license_number' in data:
                    userinfo_edit_details.license_number = data['license_number']
                if 'is_available' in data:
                    userinfo_edit_details.is_available = data['is_available']
                if 'age' in data:
                    userinfo_edit_details.age = data['age']
                if 'address' in data:
                    userinfo_edit_details.address = data['address']
                if 'photo' in data:
                    image_data = ContentFile(base64.b64decode(data['photo']))
                    file_name = str(random.randint(11111,99999))+'.jpg'
                    userinfo_edit_details.photo.save(file_name , image_data , save = True)
                #if you updated a foreign key you must save separatly for that table and save in our working table
                userinfo_edit_details.user.save()
                
                if 'is_driver' in data['userInfoAuthentication']:
                    userinfo_edit_details.userInfoAuthentication.is_driver = data['userInfoAuthentication']['is_driver']
                if 'is_customer' in data['userInfoAuthentication']:
                    userinfo_edit_details.userInfoAuthentication.is_customer = data['userInfoAuthentication']['is_customer']
                if 'is_admin' in data['userInfoAuthentication']:
                    userinfo_edit_details.userInfoAuthentication.is_admin = data['userInfoAuthentication']['is_admin']
                if 'is_employee' in data['userInfoAuthentication']:
                    userinfo_edit_details.userInfoAuthentication.is_employee = data['userInfoAuthentication']['is_admin']
                userinfo_edit_details.userInfoAuthentication.save()
                userinfo_edit_details.save()
                
                return Response('Driver details updated successfully')
        else:
            return Response({"message" : "invalid params"})


class GetUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post (self,request):
        data = request.data
        userinfo_filter = UserInfo.objects.all()
        if 'q' in data:
            userinfo_filter = UserInfo.objects.filter(user__first_name = data['q'])    
        if 'is_customer' in data:
            userinfo_filter = UserInfo.objects.filter(userInfoAuthentication__is_customer = data['is_customer'])
        if 'is_driver' in data:
            userinfo_filter = UserInfo.objects.filter(userInfoAuthentication__is_driver = data['is_driver'])
    
        userinfo_serializer  = UserInfoSerializer(userinfo_filter,many = True) #many = True
        return Response(userinfo_serializer.data)


class GetUserInfoDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        data = request.data
        userinfo_get = UserInfo.objects.get(id = data['id'])
                   
        userinfo_get_serializer = UserGetSerializer(userinfo_get)
        return Response(userinfo_get_serializer.data)


class AddCab(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        my_dict = request.data
        validation = CabValidationSerializer(data = request.data)
        if validation.is_valid():
            if 'id' not in my_dict:
                cab_form = {} 
                cab_form['make'] = my_dict['make']
                cab_form['model'] = my_dict['model']
                cab_form['year'] = my_dict['year']
                cab_form['registration_number'] = my_dict['registration_number']
                cab_form['capacity'] = my_dict['capacity']
                #you can comment the below line it , if you comment the below line, it just works fine but it will not assign the foreign key but the rest of them will be added, the foreign key will the empty in admin
                cab_form['user_id'] = my_dict['user_id']
                Cab.objects.create(**cab_form)
                return Response({"message" : "cab added successfully and also driver foreignkey is added by giving id in end point"})   #you can also use response like Response('simply okay')
            else:
                cab_record_update = Cab.objects.get(id = my_dict['id'])
                if 'make' in my_dict:
                    cab_record_update.make = my_dict['make']
                if 'model' in my_dict:
                    cab_record_update.model = my_dict['model']
                if 'year' in my_dict:
                    cab_record_update.year = my_dict['year']
                if 'registration_number' in my_dict:
                    cab_record_update.registration_number = my_dict['registration_number']
                if 'capacity' in my_dict:
                    cab_record_update.capacity = my_dict['capacity']
                # 'driver' is a foreign key variable which have the ability to access the driver table , '_id' points to the 'id'(which we cant see) of the 'driver' table 
                #you can also use the part of above method(FK) i.e. you can also edit the particular user details(first_name,last ..etc.,) because django user is a foreign key here
                if 'user_id' in my_dict:
                    cab_record_update.user_id = my_dict['user_id']  
                    
                cab_record_update.save()
                return Response({"message" : "cab details updated successfully"})
        else:
            return Response({"message" : "Mismatch of user input field"})


class GetCab(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post (self,request):
        data = request.data
        cab_filter = Cab.objects.all()
        if 'q' in data:
            cab_filter = Cab.objects.filter(model = data['q'])    #q should have model value
        if 'capacity' in data:
            cab_filter = Cab.objects.filter(capacity__gt = data['capacity'])
        if 'make' in data:
            cab_filter = Cab.objects.filter(make = data['make'])
    
        cab_serializer  = CabSerializer(cab_filter , many=True) #you can give many = true
        return Response(cab_serializer.data)


class GetCabDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        data = request.data
        cab_get = Cab.objects.get(id = data['id'])
                   
        cab_get_serializer = CabDetailsSerializer(cab_get) #many = True
        return Response(cab_get_serializer.data)


class AddBooking(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        data = request.data 
        validation = BookingValidationSerializer(data = request.data)
        if validation.is_valid():
            if 'id' not in data:
                booking_form = {} 
                booking_form['date_booked'] = data['date_booked']
                booking_form['start_location'] = data['start_location']
                booking_form['end_location'] = data['end_location']
                booking_form['start_time'] = data['start_time']
                booking_form['end_time'] = data['end_time']
                booking_form['user_id'] = data['user_id']
                booking_form['cab_id'] = data['cab_id']
                
                Booking.objects.create(**booking_form) 
                return Response('booking added')  

            else:
                booking_update_record = Booking.objects.get(id = data['id'])
                if 'date_booked' in data:
                    booking_update_record.date_booked = data['date_booked']
                if 'start_location' in data:
                    booking_update_record.start_location = data['start_location']
                if 'end_location' in data:
                    booking_update_record.end_location = data['end_location']
                if  'start_time' in data:
                    booking_update_record.start_time = data['start_time']
                if 'end_time' in data:
                    booking_update_record.end_time = data['end_time']
                if 'user_id' in data:
                    booking_update_record.user_id = data['user_id']
                if 'cab_id' in data:
                    booking_update_record.cab_id = data['cab_id'] 
                booking_update_record.save()
            
                return Response({"message" : "booking table updated successfully"})
        else:
            return Response({"message" : "invalid params"})

class GetBooking(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        data = request.data
        booking_filter = Booking.objects.all()
        if 'q' in data:
            booking_filter = Booking.objects.filter(start_location = data['q'])    #q should have start location value
        if 'date_booked' in data:
            booking_filter = Booking.objects.filter(date_booked = data['date_booked'])            
        if 'start_time' in data:
            booking_filter = Booking.objects.filter(start_time = data['start_time'])
    
        booking_serializer  = BookingSerializer(booking_filter , many = True) #you can give many = true
        return Response(booking_serializer.data)

class GetBookingDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        data = request.data
        booking_get = Booking.objects.get(id = data['id'])
                   
        booking_get_serializer = BookingDetailsSerializer(booking_get)
        return Response(booking_get_serializer.data)


# class GetCab(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         cab_query_all = Cab.objects.all()
#         cab_serializer = CabSerializer(cab_query_all , many = True)
#         return Response(cab_serializer.data)


# class GetBooking(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated/]
#     def post(self,request):
#         booking_query_all = Booking.objects.all()
#         booking_serializer = BookingSerializer(booking_query_all , many = True)
#         return Response(booking_serializer.data)
        
# # Filter() query
# class GetDriverFilter(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         data = request.data
#         driver_query_filter = Driver.objects.filter(name = data['name'])
#         booking_serializer_filter = DriverSerializerFilter(driver_query_filter , many = True)
#         return Response(booking_serializer_filter.data)


# # #getting driver photo using serializer
# # class GetDriverPhoto(APIView):
# #     def post(self,request):
# #         data = request.data 
# #         driver_photo = Driver.objects.get(name = data['name'])
# #         driver_photo_serializer = DriverPhotoSerializer(driver_photo.photo.read())
# #         return Response(driver_photo_serializer.data)

# class GetCustomerFilter(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         data = request.data
#         customer_query_filter = Customer.objects.filter(name = data['name'])
#         customer_serializer_filter = CustomerSerializerFilter(customer_query_filter , many = True)
#         return Response(customer_serializer_filter.data)
    
# class GetCustomerContain(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         my_dict = request.data
#         customer_query_contain = Customer.objects.filter(name__contains = my_dict['contains'])
#         customer_serializer_contain = CustomerSerializerContain(customer_query_contain , many = True)
#         return Response(customer_serializer_contain.data)
    
# class GetBookingOrder(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         booking_query_order = Booking.objects.all().order_by('start_location')
#         booking_serializer_order = BookingSerializerOrder(booking_query_order , many = True)
#         return Response(booking_serializer_order.data)
# #You can first(),last() by replacing 'all().order_by('') and many = False
# # from django.contrib.auth.models import User

            
# class AddCustomer(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self,request):
#         data = request.data
#         validation = CustomerValidationSerializer(data = data)
#         if validation.is_valid():
#             if 'id' not in data:
#                 if User.objects.filter(email = data['user']['email']).count()==0:
#                     user = User.objects.create(first_name = data['user']['first_name'] , last_name = data['user']['last_name'] , email = data['user']['email'] , username = data['user']['email'],password = data['user']['password'])
                
#                     customer_form = {}
#                     customer_form['contact_number'] = data['contact_number']
#                     customer_form['address'] = data['address']
                    
#                     Customer.objects.create(**customer_form , user = user)
                    
#                     return Response({"message" : "customer form added successfully"})
#                 else:
#                     return Response({"message" : "user(email) is already exist"})
#             else:
#                 customer_update_record = Customer.objects.get(id = data['id'])
#                 if 'first_name' in data['user']:
#                     customer_update_record.user.first_name = data['user']['first_name']
#                 if 'last_name' in data['user']:
#                     customer_update_record.user.last_name = data['user']['last_name']
#                 if 'contact_number' in data:
#                     customer_update_record.contact_number = data['contact_number']
#                 if 'address' in data:
#                     customer_update_record.address = data['address']
#                 customer_update_record.user.save()
                    
#                 customer_update_record.save()
#                 return Response('customer record updated successfully')
#         else:
#             return Response({"message" : "Invalid user input fields"})

# class AddCab(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request):
#         my_dict = request.data
#         validation = CabValidationSerializer(data = request.data)
#         if validation.is_valid():
#             if 'id' not in my_dict:
#                 cab_form = {} 
#                 cab_form['make'] = my_dict['make']
#                 cab_form['model'] = my_dict['model']
#                 cab_form['year'] = my_dict['year']
#                 cab_form['registration_number'] = my_dict['registration_number']
#                 cab_form['capacity'] = my_dict['capacity']
#                 #you can comment the below line it , if you comment the below line, it just works fine but it will not assign the foreign key but the rest of them will be added, the foreign key will the empty in admin
#                 cab_form['driver_id'] = my_dict['driver_id']
#                 Cab.objects.create(**cab_form)
#                 return Response({"message" : "cab added successfully and also driver foreignkey is added by giving id in front end"})   #you can also use response like Response('okay')
#             else:
#                 cab_record_update = Cab.objects.get(id = my_dict['id'])
#                 if 'make' in my_dict:
#                     cab_record_update.make = my_dict['make']
#                 if 'model' in my_dict:
#                     cab_record_update.model = my_dict['model']
#                 if 'year' in my_dict:
#                     cab_record_update.year = my_dict['year']
#                 if 'registration_number' in my_dict:
#                     cab_record_update.registration_number = my_dict['registration_number']
#                 if 'capacity' in my_dict:
#                     cab_record_update.capacity = my_dict['capacity']
#                 # 'driver' is a foreign key variable which have the ability to access the driver table'_id' points to the 'id'(which we cant see) of the 'driver' table 
#                 if 'driver_id' in my_dict:
#                     cab_record_update.driver_id = my_dict['driver_id']  
#                 cab_record_update.save()
#                 return Response({"message" : "cab details updated successfully"})
#         else:
#             return Response({"message" : "Mismatch of user input field"})
            
    
# class AddBooking(APIView):
#     #that above AddCab class used for just giving a value to database through postman, but what if inserting table has foreign keys for that we can't just like that insert like the above method. so this AddBooking class will do that. there are two types 1. just bring the existing id of one of record of foreign table to map or 2. if we want to create a new record in the booking table as well as we need new value for that. Here (AddBooking) we done 2nd method the 1st first will be done in AddBooking
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request):
#         data = request.data 
#         validation = BookingValidationSerializer(data = request.data)
#         if validation.is_valid():
#             if 'id' not in data:
#                 booking_form = {} 
#                 booking_form['date_booked'] = data['date_booked']
#                 booking_form['start_location'] = data['start_location']
#                 booking_form['end_location'] = data['end_location']
#                 booking_form['start_time'] = data['start_time']
#                 booking_form['end_time'] = data['end_time']
                
#                 #customer is a foreign key in Booking table
#                 customer_form = {}
#                 customer_form['name'] = data['customer']['name']
#                 customer_form['contact_number'] = data['customer']['contact_number']
#                 customer_form['email'] = data['customer']['email']
#                 customer_form['address'] = data['customer']['email']
#                 #first adding this new record to its table and they only we can use it as foreignkey 
#                 customer = Customer.objects.create(**customer_form) 
#                 #in create() we sending the booking which is we are doing but it has two foreign keys customer and cab(see in cab model) first now we are giving input for the customer table
#                 Booking.objects.create(**booking_form , customer = customer)
#                 return Response('booking added')  
#                 # hdhdhdhd
#                 # #for 2nd foreign key "cab" in booking table
#                 # cab_form = {}
#                 # cab_form['make'] = data['cab']['make']
#                 # cab_form['model'] = data['cab']['model']
#                 # cab_form['year'] = data['cab']['year']
#                 # cab_form['registration_number'] = data['cab']['registration_number']
#                 # cab_form['capacity'] = data['cab']['capacity']
                
#                 # #this is for cab's foreign key
#                 # driver_form = {}
#                 # driver_form['name'] = data['cab']['driver']['name']
#                 # driver_form['contact_number'] = data['cab']['driver']['contact_number']
#                 # driver_form['email'] = data['cab']['driver']['email']
#                 # driver_form['license_number'] = data['cab']['driver']['license_number']
#                 # driver_form['is_available'] = data['cab']['driver']['is_available']
#                 # driver_form['age'] = data['cab']['driver']['age']
#             else:
#                 booking_update_record = Booking.objects.get(id = data['id'])
#                 if 'date_booked' in data:
#                     booking_update_record.date_booked = data['date_booked']
#                 if 'start_location' in data:
#                     booking_update_record.start_location = data['start_location']
#                 if 'end_location' in data:
#                     booking_update_record.end_location = data['end_location']
#                 if  'start_time' in data:
#                     booking_update_record.start_time = data['start_time']
#                 if 'end_time' in data:
#                     booking_update_record.end_time = data['end_time']
#                 if 'customer_id' in data:
#                     booking_update_record.customer_id = data['customer']
#                 if 'cab_id' in data:
#                     booking_update_record.cab_id = data['cab_id'] 
#                 booking_update_record.save()
            
#                 return Response({"message" : "booking table updated successfully"})
#         else:
#             return Response({"message" : "invalid params"})
        
        
#serialization
#we have to create class instead of def coz we are doing serialization
# all() queries
# class GetDriver(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         data = request.data
#         driver_query_all = UserInfo.objects.filter(name = data['name'])
#         driver_serializer = DriverSerializer(driver_query_all , many = True)
#         return Response(driver_serializer.data)
    
# class GetCustomer(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         customer_query_all = UserInfo.objects.all()
#         customer_serializer = CustomerSeralizer(customer_query_all , many = True)
#         return Response(customer_serializer.data)

# def do_all(request):
#     extracted = Driver.objects.all()
#     context = {
#     }
#     got_template = loader.get_template('query_template.html')
#     return HttpResponse(got_template.render(context,request))

# return HttpResponse('Hello from cabmanagement views file')

# class AddDriver(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self,request):
#         data = request.data
#         #validation
#         validation = DriverValidationSerializer(data = request.data)
#         if validation.is_valid():
#             if 'id' not in data:
#                 if User.objects.filter(email = data['user']['email']).count() == 0:
#                     driver_form = {}
#                     driver_form['contact_number'] = data['contact_number']
#                     driver_form['license_number'] = data['license_number']
#                     driver_form['is_available'] = data['is_available']
#                     driver_form['age'] = data['age']
#                     #photo
#                     #driver_form['photo'] = data['s']
#                     if 'photo' in data: 
#                         image_data = ContentFile(base64.b64decode(data['photo']))
#                         file_name = str(random.randint(11111,99999))+'.jpg'
#                         driver = Driver.objects.create(**driver_form)  #**means it sends as keyword arguments(means key value pair)
#                         driver.photo.save(file_name , image_data , save = True)
                        
#                     user_form = {}
#                     user_form['first_name'] = data['user']['first_name']
#                     user_form['last_name'] = data['user']['last_name']
#                     user_form['email'] = data['user']['email']
#                     user_form['username'] = data['user']['email']
#                     user_form['password'] = data['user']['password']
                    
#                     user = User.objects.create(**user_form)
#                     Driver.objects.create(**driver_form , user = user)
                    
#                     return Response({"Message":"Driver form added successfully"})
#                 else:
#                     return Response({"message" : "user(email) is already existed"})
#             else:
#                 driver_edit_details = Driver.objects.get(id = data['id'])
#                 if 'first_name' in data['user']: 
#                     driver_edit_details.user.first_name = data['user']['first_name']
#                 if 'last_name' in data['user']:
#                     driver_edit_details.user.last_name = data['user']['last_name']

#                 if 'contact_number' in data:
#                     driver_edit_details.contact_number = data['contact_number']
#                 if 'license_number' in data:
#                     driver_edit_details.license_number = data['license_number']
#                 if 'is_available' in data:
#                     driver_edit_details.is_available = data['is_available']
#                 if 'age' in data:
#                     driver_edit_details.age = data['age']
#                 if 'photo' in data:
#                     image_data = ContentFile(base64.b64decode(data['photo']))
#                     file_name = str(random.randint(11111,99999))+'.jpg'
#                     driver_edit_details.photo.save(file_name , image_data , save = True)
#                 #if you updated a foreign key you must save separatly for that table(which has foreign key) and save in our working table
#                 driver_edit_details.user.save()
#                 driver_edit_details.save()
#                 return Response('Driver details updated successfully')
#         else:
#             return Response({"message" : "invalid params"})




# def do_hello(request):
#     #var = .objects.all()
#     templates = loader.get_template('hello.html')
#     return HttpResponse(templates.render())


# def do_get_filter(request):
#     get_extracted = UserInfo.objects.get(name = 'rajesh')
#     filter_extracted = UserInfo.objects.filter(age__lte = 25 , name = 'Thulasivasan') #for multiple conditions put ','(comma) in btw contions and it works as 'and' operator... so if multiple or use 'Q' object django.db.models

#     get_filter_dict = {
#         'key_get' : get_extracted , 
#         'key_filter' : filter_extracted
#     }

#     got_template = loader.get_template('get_filter.html')
#     return HttpResponse(got_template.render(get_filter_dict , request))

# def do_query(request):
#     all_extracted = UserInfo.objects.all()
#     order_extracted = UserInfo.objects.order_by('-age')  #1. '-' it mentions descending order 2.it uses no assisgning operator like others  3.enter column name as a string
#     exclude_extracted = UserInfo.objects.exclude(name = 'Thulasivasan')  #exclude is like 'not' operator
#     q_extracted = UserInfo.objects.filter(Q(age__gt = 18) | Q(name__contains = 'Thulasivasan'))  #1. '|' this means 'or' 2.This allows if record's age > 25 or having name as 'Sathish'

#     values_list_extracted = UserInfo.objects.values_list('name' , flat = True)  #column name as string
#     first_extracted = UserInfo.objects.first()
#     last_extracted = UserInfo.objects.last()

#     #use filter function whenever you use delete function
#     UserInfo.objects.filter(name__contains = 'Sathish').delete()
#     after_delete = UserInfo.objects.all()


#     do_query_dict = {
#         'key_all' : all_extracted,
#         'key_order' : order_extracted , 
#         'key_exclude' : exclude_extracted ,
#         'key_q' : q_extracted,
#         'key_values_list' : values_list_extracted,
#         'key_first' : first_extracted,
#         'key_last' : last_extracted,
#         'key_after' : after_delete,
#         'key_all' : all_extracted

#     }
#     got_template = loader.get_template('query_template.html')
#     return HttpResponse(got_template.render(do_query_dict, request))

# class GetCustomers(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         #Accessing a foreign keys table by using 
#         customer_details = UserInfo.objects.filter(userInfoAuthentication__is_customer = True)
        
#         customer_only_serializer = CustomerInfoSerializer(customer_details , many = True)
#         return Response(customer_only_serializer.data)

# class GetSearch(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         customerq = UserInfo.objects.filter()    


# class GetDrivers(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#     #     driver_only = UserInfoAuthentication.objects.filter(is_driver = True)
#     #     driver_details = UserInfo.objects.filter(id = driver_only.id)
#         if 'q' in data:
#             driver_details = UserInfo.ob
#         driver_details = UserInfo.objects.filter(userInfoAuthentication__is_driver = True)
#         driver_only_serializer = CustomerInfoSerializer(driver_details , many = True)
#         return Response(driver_only_serializer.data)
