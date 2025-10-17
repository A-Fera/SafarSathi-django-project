from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Destination reviews
    path('destinations/<int:destination_id>/review/', views.destination_review, name='destination_review'),
    path('destinations/<int:destination_id>/reviews/', views.destination_review_list, name='destination_review_list'),

    # Accommodation reviews
    path('accommodations/<int:accommodation_id>/review/', views.accommodation_review, name='accommodation_review'),
    path('accommodations/<int:accommodation_id>/reviews/', views.accommodation_review_list,
         name='accommodation_review_list'),
]