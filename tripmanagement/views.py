from django.shortcuts import render
# Create your views here.
from . models import *
from rest_framework.views import APIView
from . trip_response_serializer import *
from rest_framework.response import Response

from . trip_request_serializer import *

#for using authentication
from rest_framework import authentication , permissions

class AddTrip(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self , request):
        data = request.data
        validation = TripValidationSerializer(data = data)
        if validation.is_valid():
            if 'id' not in data:
                trip_form = {}
                trip_form['date_started'] = data['date_started']
                trip_form['date_ended'] = data['date_ended']        
                trip_form['total_distance'] = data['total_distance']
                trip_form['total_cost'] = data['total_cost']
                trip_form['is_completed'] = data['is_completed']
                #foreign key are adding
                trip_form['user_driver_fk_id'] = data['user_driver_fk_id']
                trip_form['user_customer_fk_id'] = data['user_customer_fk_id']
                trip_form['cab_id'] = data['cab_id']
                trip_form['booking_id'] = data['booking_id']
                Trip.objects.create(**trip_form)
                return Response({"message" : "Trip form has been added successfully"})
            else:
                trip_record_update = Trip.objects.get(id = data['id'])  #id = the left id represents the column
                if 'date_started' in data:
                    trip_record_update.date_started = data['date_started']
                if 'date_ended' in data:
                    trip_record_update.date_ended = data['date_ended']
                if 'total_distance' in data:
                    trip_record_update.total_distance = data['total_distance']
                if 'total_cost' in data:
                    trip_record_update.total_cost = data['total_cost']
                if 'is_completed' in data:
                    trip_record_update.is_completed = data['is_completed']
                if 'driver_id' in data:
                    trip_record_update.user_driver_fk_id = data['user_driver_fk_id']  #driver_id(foreign key) will be white 
                if 'customer_id' in data:
                    trip_record_update.user_customer_fk_id = data['user_customer_fk']
                if 'cab_id' in data:
                    trip_record_update.cab_id = data['cab_id']
                if 'booking_id' in data:
                    trip_record_update.booking_id = data['booking_id']
                return Response({"message" : "Trip table updated successfully"})
        else:
            return Response({"message" : "Invalid params"})
        
class GetTrip(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        data = request.data
        trip_filter = Trip.objects.all()
        if 'q' in data:
            trip_filter = Trip.objects.filter(total_cost = data['q'])    #q should have total cost value
        if 'total_distance' in data:
            trip_filter = Trip.objects.filter(total_distance = data['total_distance'])
        if 'date_started' in data:
            trip_filter = Trip.objects.filter(date_started = data['date_started'])
    
        trip_serializer  = TripSerializer(trip_filter , many = True) #you can give many = true
        return Response(trip_serializer.data)

class GetTripDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        data = request.data
        trip_get = Trip.objects.get(id = data['id'])
                   
        trip_get_serializer = TripDetailsSerializer(trip_get)
        return Response(trip_get_serializer.data)

            
class AddReview(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request):
        data = request.data 
        validation = ReviewValidationSerializer(data = request.data)
        if validation.is_valid():
            if 'id' not in data:
                review_form = {}
                review_form['customer_name'] = data['customer_name']
                review_form['review_text'] = data['review_text']
                review_form['rating'] = data['rating']
                review_form['date_posted'] = data['date_posted']   #give data in the format of 'YYYY-MM-DD' in a string format
                #foreign key
                review_form['trip_id'] = data['trip_id']
                manyfield_driver_ids = data['manyfield_driver_ids']
                
                initial_review = Review.objects.create(**review_form)
                initial_review.user_manyfield.add(*manyfield_driver_ids)
                return Response({"Message to postman" : "Customer's review record added successfully"})
            else:
                review_record_update = Review.objects.get(id = data['id'])
                
                if 'customer_name' in data:
                    review_record_update.customer_name = data['customer_name']
                if 'review_text' in data:
                    review_record_update.review_text = data['review_text']
                if 'rating' in data:
                    review_record_update.rating = data['rating']
                if 'date_posted' in data:
                    review_record_update.date_posted = data['date_posted']
                #updating the foreign key(below line)
                if 'trip_id' in data:
                    review_record_update.trip_id = data['trip_id']
                if 'manyfield_driver_ids'  in data:
                    review_record_update.user_manyfield.set(data['manyfield_driver_ids'])
                review_record_update.save()
                return Response('Review record edited successfully')
        else:
            return Response({"message" : "invalid params"})


class GetReview(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        data = request.data
        review_filter = Review.objects.all()
        if 'q' in data:
            review_filter = Review.objects.filter(customer_name = data['q'])    #q should have total cost value
        if 'total_distance' in data:
            review_filter = Review.objects.filter(rating = data['rating'])
        if 'date_started' in data:
            review_filter = Review.objects.filter(trip__total_cost = data['total_cost']) #accessing  foreign key's value in filter
    
        review_serializer  = ReviewSerializer(review_filter , many = True) #you can give many = true
        return Response(review_serializer.data)

class GetReviewDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        data = request.data
        review_get = Review.objects.get(id = data['id'])
                   
        review_get_serializer = ReviewDetailsSerializer(review_get , many = False)
        return Response(review_get_serializer.data)


        
# class GetTrip(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request):
#         trip_query_all = Trip.objects.all()
#         trip_serializer = TripSerializer(trip_query_all , many = True)
#         return Response(trip_serializer.data)
    
# class GetReview(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request):
#         review_query_all = Review.objects.all()
#         review_serializer = ReviewSerializer(review_query_all , many = True)
#         return Response(review_serializer.data)
    
