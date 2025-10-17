from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from destinations.models import Destination
from bookings.models import Accommodation
from .models import DestinationReview, AccommodationReview, ReviewPhoto
from .forms import DestinationReviewForm, AccommodationReviewForm, ReviewPhotoForm


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
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('bookings:accommodation_detail', pk=accommodation_id)
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
        form = DestinationReviewForm()

    return render(request, 'reviews/destination_review_form.html', {
        'form': form,
        'destination': destination
    })