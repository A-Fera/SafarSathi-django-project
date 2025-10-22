from django.db import models
from accounts.models import User

# Create your models here.
class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('historical', 'Historical'),
        ('natural', 'Natural'),
        ('religious', 'Religious'),
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('wildlife', 'Wildlife'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100, default='Bangladesh')
    best_time_to_visit = models.CharField(max_length=200)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Photo(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='destinations/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.destination.name} - {self.caption}"
