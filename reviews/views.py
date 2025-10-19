from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from destinations.models import Destination
from bookings.models import Accommodation
from accounts.models import LocalGuide
from .models import DestinationReview, AccommodationReview, GuideReview, ReviewPhoto
from .forms import DestinationReviewForm, AccommodationReviewForm, GuideReviewForm, ReviewPhotoForm


@login_required
def destination_review(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)

    # Check if user already reviewed this destination
    if DestinationReview.objects.filter(destination=destination, user=request.user).exists():
        messages.error(request, 'You have already reviewed this destination.')
        return redirect('destinations:destination_detail', pk=destination_id)

    if request.method == 'POST':
        form = DestinationReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('destinations:destination_detail', pk=destination_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DestinationReviewForm()

    return render(request, 'reviews/destination_review_form.html', {
        'form': form,
        'destination': destination
    })


def destination_review_list(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    reviews = DestinationReview.objects.filter(
        destination=destination,
        is_approved=True
    ).order_by('-created_at')

    return render(request, 'reviews/destination_review_list.html', {
        'destination': destination,
        'reviews': reviews
    })


@login_required
def accommodation_review(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)

    # Check if user already reviewed this accommodation
    if AccommodationReview.objects.filter(accommodation=accommodation, user=request.user).exists():
        messages.error(request, 'You have already reviewed this accommodation.')
        return redirect('bookings:accommodation_detail', pk=accommodation_id)

    if request.method == 'POST':
        form = AccommodationReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.accommodation = accommodation
            review.save()

            # Update accommodation's average rating
            reviews = AccommodationReview.objects.filter(accommodation=accommodation, is_approved=True)
            if reviews.exists():
                avg_rating = sum(review.rating for review in reviews) / reviews.count()
                accommodation.rating = round(avg_rating, 1)
                accommodation.save()

            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('bookings:accommodation_detail', pk=accommodation_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccommodationReviewForm()

    return render(request, 'reviews/accommodation_review_form.html', {
        'form': form,
        'accommodation': accommodation
    })


def accommodation_review_list(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    reviews = AccommodationReview.objects.filter(
        accommodation=accommodation,
        is_approved=True
    ).order_by('-created_at')

    return render(request, 'reviews/accommodation_review_list.html', {
        'accommodation': accommodation,
        'reviews': reviews
    })


@login_required
def guide_review(request, guide_id):
    guide = get_object_or_404(LocalGuide, pk=guide_id)

    # Check if user already reviewed this guide
    if GuideReview.objects.filter(guide=guide, user=request.user).exists():
        messages.error(request, 'You have already reviewed this guide.')
        return redirect('accounts:guide_detail', pk=guide_id)

    if request.method == 'POST':
        form = GuideReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.guide = guide
            review.save()

            # Update guide's average rating
            reviews = GuideReview.objects.filter(guide=guide, is_approved=True)
            if reviews.exists():
                avg_rating = sum(review.rating for review in reviews) / reviews.count()
                guide.rating = round(avg_rating, 1)
                guide.save()

            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('accounts:guide_detail', pk=guide_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GuideReviewForm()

    return render(request, 'reviews/guide_review_form.html', {
        'form': form,
        'guide': guide
    })


def guide_review_list(request, guide_id):
    guide = get_object_or_404(LocalGuide, pk=guide_id)
    reviews = GuideReview.objects.filter(
        guide=guide,
        is_approved=True
    ).order_by('-created_at')

    return render(request, 'reviews/guide_review_list.html', {
        'guide': guide,
        'reviews': reviews
    })
