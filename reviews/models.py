from django.db import models
from django.contrib.auth import get_user_model
from destinations.models import Destination
from bookings.models import Accommodation
from accounts.models import LocalGuide


# Create your models here.


User = get_user_model()


class DestinationReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('destination', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.destination.name}"

    @property
    def title(self):
        """Generate a title based on rating"""
        rating_titles = {
            1: "Poor Experience",
            2: "Below Average",
            3: "Average Experience",
            4: "Good Experience",
            5: "Excellent Experience"
        }
        return rating_titles.get(self.rating, "Review")


class AccommodationReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('accommodation', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.accommodation.name}"

    @property
    def title(self):
        """Generate a title based on rating"""
        rating_titles = {
            1: "Poor Stay",
            2: "Below Average Stay",
            3: "Average Stay",
            4: "Good Stay",
            5: "Excellent Stay"
        }
        return rating_titles.get(self.rating, "Review")


class GuideReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    guide = models.ForeignKey(LocalGuide, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('guide', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.guide.user.get_full_name()}"

    @property
    def title(self):
        """Generate a title based on rating"""
        rating_titles = {
            1: "Poor Service",
            2: "Below Average Guide",
            3: "Average Guide Experience",
            4: "Good Guide Service",
            5: "Excellent Guide Service"
        }
        return rating_titles.get(self.rating, "Review")


class ReviewPhoto(models.Model):
    destination_review = models.ForeignKey(DestinationReview, on_delete=models.CASCADE, related_name='photos',
                                           null=True, blank=True)
    accommodation_review = models.ForeignKey(AccommodationReview, on_delete=models.CASCADE, related_name='photos',
                                             null=True, blank=True)
    guide_review = models.ForeignKey(GuideReview, on_delete=models.CASCADE, related_name='photos',
                                     null=True, blank=True)
    image = models.ImageField(upload_to='review_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.destination_review:
            return f"Photo for {self.destination_review.title}"
        elif self.accommodation_review:
            return f"Photo for {self.accommodation_review.title}"
        elif self.guide_review:
            return f"Photo for {self.guide_review.title}"
        return "Review Photo"
