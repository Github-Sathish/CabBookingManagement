from rest_framework import serializers

from cabmanagement.models import *

import uuid
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields ='__all__'
    
    
class TripValidationSerializer(serializers.Serializer):
    date_started = serializers.DateField(required = True)
    date_ended = serializers.DateField(required = True)
    total_distance = serializers.IntegerField(required = True)
    total_cost = serializers.IntegerField(required = True)
    is_completed = serializers.BooleanField(required = True)
    user_driver_fk_id = serializers.UUIDField(required = True)
    user_customer_fk_id = serializers.UUIDField(required = True)
    cab_id = serializers.UUIDField(required = True)
    booking_id = serializers.UUIDField(required = True)

class ReviewValidationSerializer(serializers.Serializer):
    customer_name = serializers.CharField(required = True)
    review_text = serializers.CharField(required = True)   #Charfield = TextField 
    rating = serializers.IntegerField(required = True)
    date_posted = serializers.DateField(required = True)
    trip_id = serializers.UUIDField(required = True)
    # review_driver_manyfield = serializers.ManyToManyField(UserInfo)
    review_driver_manyfield = UserInfoSerializer(required = True) 
    
# class ReviewValidationSerializer(serializers.Serializer):
#     customer_name = serializers.CharField(max_length=200)
#     review_text = serializers.CharField(allow_blank=True, required=False)
#     rating = serializers.IntegerField(min_value=1, max_value=5)
#     date_posted = serializers.DateField(format="%Y-%m-%d")
#     trip_id = serializers.UUIDField(required = True)
#     manyfield_driver_ids = serializers.ListField(child=serializers.UUIDField())

#     def validate_manyfield_driver_ids(self, value):
#         """
#         Custom validation for manyfield_driver_ids.
#         Ensure that each ID in the list is a valid UUID.
#         """
#         for driver_id in value:
#             try:
#                 uuid.UUID(driver_id)
#             except ValueError:
#                 raise serializers.ValidationError("Invalid UUID format for driver_id")
#         return value