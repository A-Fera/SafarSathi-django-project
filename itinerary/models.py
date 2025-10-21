from django.db import models
from django.contrib.auth import get_user_model
from destinations.models import Destination
from bookings.models import Accommodation

User = get_user_model()


class Itinerary(models.Model):
    TRIP_STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=TRIP_STATUS_CHOICES, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Itineraries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_destinations(self):
        return self.itinerary_items.values('destination').distinct().count()


class ItineraryItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('destination', 'Destination Visit'),
        ('accommodation', 'Accommodation'),
    ]

    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='itinerary_items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='destination')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['start_date', 'order']

    def __str__(self):
        return f"{self.title} - {self.itinerary.title}"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1


