from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Accommodation views
    path('accommodations/', views.AccommodationListView.as_view(), name='accommodation_list'),
    path('accommodations/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('accommodations/create/', views.accommodation_create, name='accommodation_create'),
    path('accommodations/<int:pk>/update/', views.accommodation_update, name='accommodation_update'),
    path('accommodations/<int:pk>/delete/', views.accommodation_delete, name='accommodation_delete'),


]
