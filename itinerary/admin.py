from django.contrib import admin
from .models import Itinerary, ItineraryItem, ItineraryCollaborator

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1
    fields = ['item_type', 'title', 'destination', 'start_date', 'end_date', 'estimated_cost']

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['title', 'user__username', 'description']
    inlines = [ItineraryItemInline]
    date_hierarchy = 'start_date'

@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'itinerary', 'item_type', 'start_date', 'end_date', 'estimated_cost']
    list_filter = ['item_type', 'start_date']
    search_fields = ['title', 'itinerary__title']


