
from django.db import models
from django.contrib.auth import get_user_model
from destinations.models import Destination
# Create your models here.
User = get_user_model()


class Accommodation(models.Model):
    ACCOMMODATION_TYPES = [
        ('hotel', 'Hotel'),
        ('guesthouse', 'Guest House'),
        ('resort', 'Resort'),
        ('homestay', 'Homestay'),
        ('hostel', 'Hostel'),
        ('apartment', 'Apartment'),
    ]

    name = models.CharField(max_length=200)
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_TYPES)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accommodations')
    address = models.TextField()
    description = models.TextField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField(default=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to='accommodations/', blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='11:00')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


