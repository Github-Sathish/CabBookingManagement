from rest_framework import serializers


class UserInfoValidationSerializer(serializers.Serializer):
    license_number = serializers.CharField(required = False)
    contact_number = serializers.IntegerField(required = False)
    address = serializers.CharField(required = True)
    #photo = serializers.ImageField(required  = False)
    age = serializers.IntegerField(required  = False)
    #FKs
    user_id = serializers.UUIDField(required = False)
    userInfoAuthentication_id = serializers.UUIDField(required = False)
 
    
class CabValidationSerializer(serializers.Serializer):
    make = serializers.CharField(required = True)
    model = serializers.CharField(required = True)   
    year = serializers.IntegerField(required = True)
    registration_number = serializers.CharField(required = True)
    capacity = serializers.IntegerField(required = True)
    
    #user_id = serializers.UUIDField(required = True)


class CustomerValidationSerializer(serializers.Serializer):
    # name = serializers.CharField(required = True)
    contact_number = serializers.CharField(required = True)
    #email = serializers.EmailField(required = True)
    address = serializers.CharField(required = True)  #CharField = TextField


class BookingValidationSerializer(serializers.Serializer):
    date_booked = serializers.DateTimeField(required = True)
    start_location = serializers.CharField(required = True)
    end_location = serializers.CharField(required = True)
    start_time = serializers.TimeField(required = True)
    end_time = serializers.TimeField(required = True)
    user_id = serializers.UUIDField(required = False)
    cab_id = serializers.UUIDField(required = False)



# class DriverValidationSerializer(serializers.Serializer):
#     # name = serializers.CharField(required = True)
#     contact_number = serializers.CharField(required = True)
#     # email = serializers.EmailField(required = True)
#     license_number = serializers.CharField(required = True)
#     is_available = serializers.BooleanField(required = True)
#     #photo = serializers.ImageField(required = False)
#     age = serializers.IntegerField(required = True)