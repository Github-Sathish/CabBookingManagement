from django.urls import path
from . import views


urlpatterns = [
    # path('getTripAll/', views.GetTrip.as_view() , name = 'getTripAll'),
    # path('getReviewAll/' , views.GetReview.as_view() , name = 'getReviewAll'),
    # path('addReview/' , views.AddReview.as_view() , name = 'Adding a new review through API'),
    # path('addTrip/' , views.AddTrip.as_view() , name = 'Adding a new trip through API')
    path('addTrip/' , views.AddTrip.as_view() , name = 'addTrip'),
    path('getTrip/' , views.GetTrip.as_view() , name = 'getTrip'),
    path('getTripDetails/' , views.GetTripDetails.as_view() , name = 'getTripDetails'),
    path('addReview/' , views.AddReview.as_view() , name = 'addReview'),
    path('getReview/' , views.GetReview.as_view() , name = 'getReview'),
    path('getReviewDetails/' , views.GetReviewDetails.as_view() , name = 'getReviewDetails'),
]
