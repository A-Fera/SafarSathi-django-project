from django.contrib import admin
from .models import Destination, Photo

# Register your models here.
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location',  'created_at']
    list_filter = ['category',  'created_at']
    search_fields = ['name', 'location', 'description']



@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['destination', 'caption', 'uploaded_by', 'uploaded_at']
    list_filter = [ 'uploaded_at', 'destination']
    search_fields = ['destination__name', 'caption']
