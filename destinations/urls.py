from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    # List view
    path('', views.DestinationListView.as_view(), name='destination_list'),

    # Detail view
    path('<int:pk>/', views.destination_detail, name='destination_detail'),

    # Create view
    path('create/', views.destination_create, name='destination_create'),

    # Update view
    path('<int:pk>/update/', views.destination_update, name='destination_update'),

    # Delete view - new
    path('<int:pk>/delete/', views.destination_delete, name='destination_delete'),

    # Photo upload
    path('<int:destination_pk>/upload-photo/', views.photo_upload, name='photo_upload'),
]