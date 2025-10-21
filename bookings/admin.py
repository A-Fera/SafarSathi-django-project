from django.contrib import admin
from .models import Accommodation
# Register your models here.
@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'accommodation_type', 'destination', 'price_per_night', 'rating', 'is_available']
    list_filter = ['accommodation_type', 'destination', 'is_available', 'created_at']
    search_fields = ['name', 'destination__name', 'address']

