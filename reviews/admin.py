from django.contrib import admin
from .models import DestinationReview, AccommodationReview, GuideReview, ReviewPhoto

# Register your models here.
class ReviewPhotoInline(admin.TabularInline):
    model = ReviewPhoto
    extra = 1


@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['destination__name', 'user__username', 'content']
    inlines = [ReviewPhotoInline]
    actions = ['approve_reviews', 'disapprove_reviews']

    def title(self, obj):
        return obj.title
    title.short_description = 'Title'

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(AccommodationReview)
class AccommodationReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'accommodation', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['accommodation__name', 'user__username', 'content']
    inlines = [ReviewPhotoInline]
    actions = ['approve_reviews', 'disapprove_reviews']

    def title(self, obj):
        return obj.title
    title.short_description = 'Title'

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(GuideReview)
class GuideReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'guide', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['guide__user__username', 'guide__user__first_name', 'guide__user__last_name', 'user__username', 'content']
    inlines = [ReviewPhotoInline]
    actions = ['approve_reviews', 'disapprove_reviews']

    def title(self, obj):
        return obj.title
    title.short_description = 'Title'

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(ReviewPhoto)
class ReviewPhotoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'get_review_title', 'uploaded_at']
    list_filter = ['uploaded_at']

    def get_review_title(self, obj):
        if obj.destination_review:
            return obj.destination_review.title
        elif obj.accommodation_review:
            return obj.accommodation_review.title
        elif obj.guide_review:
            return obj.guide_review.title
        return "No review"

    get_review_title.short_description = 'Review'
