from django.urls import path
from . import views

app_name = 'itinerary'

urlpatterns = [
   
    path('', views.itinerary_list, name='itinerary_list'),
    path('create/', views.itinerary_create, name='itinerary_create'),
    path('<int:pk>/', views.itinerary_detail, name='itinerary_detail'),
    path('<int:pk>/update/', views.itinerary_update, name='itinerary_update'),
    path('<int:pk>/delete/', views.itinerary_delete, name='itinerary_delete'),

    
    path('<int:itinerary_pk>/add-item/', views.item_create, name='item_create'),
    path('<int:itinerary_pk>/item/<int:item_pk>/update/', views.item_update, name='item_update'),
    path('<int:itinerary_pk>/item/<int:item_pk>/delete/', views.item_delete, name='item_delete'),



]
