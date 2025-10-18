from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q, Avg
from datetime import datetime, timedelta
from .models import Accommodation, Booking
from .forms import AccommodationForm, BookingForm
from reviews.models import AccommodationReview


# Create your views here.
class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'bookings/accommodation_list.html'
    context_object_name = 'accommodations'
    paginate_by = 12

    def get_queryset(self):
        queryset = Accommodation.objects.filter(is_available=True).order_by('-created_at')
        search = self.request.GET.get('search')
        accommodation_type = self.request.GET.get('type')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(destination__name__icontains=search) |
                Q(address__icontains=search)
            )

        if accommodation_type:
            queryset = queryset.filter(accommodation_type=accommodation_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accommodation_types'] = Accommodation.ACCOMMODATION_TYPES
        return context


def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    reviews = AccommodationReview.objects.filter(
        accommodation=accommodation,
        is_approved=True
    ).order_by('-created_at')[:10]

    # Check if user has booked this accommodation and can review
    user_can_review = False
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_booked = Booking.objects.filter(
            accommodation=accommodation,
            user=request.user,
            booking_status='confirmed'
        ).exists()

        user_has_reviewed = AccommodationReview.objects.filter(
            accommodation=accommodation,
            user=request.user
        ).exists()

        user_can_review = user_has_booked and not user_has_reviewed

    context = {
        'accommodation': accommodation,
        'reviews': reviews,
        'user_can_review': user_can_review,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'bookings/accommodation_detail.html', context)


@login_required
def accommodation_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add accommodations.')
        return redirect('bookings:accommodation_list')

    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.created_by = request.user
            accommodation.save()
            messages.success(request, 'Accommodation created successfully!')
            return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    else:
        form = AccommodationForm()

    return render(request, 'bookings/accommodation_form.html', {'form': form, 'title': 'Add New Accommodation'})


@login_required
def accommodation_update(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.user != accommodation.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this accommodation.')
        return redirect('bookings:accommodation_detail', pk=pk)

    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES, instance=accommodation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accommodation updated successfully!')
            return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    else:
        form = AccommodationForm(instance=accommodation)

    return render(request, 'bookings/accommodation_form.html', {
        'form': form,
        'title': 'Update Accommodation'
    })


@login_required
def accommodation_delete(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)

    # Check if user has permission to delete
    if request.user != accommodation.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this accommodation.')
        return redirect('bookings:accommodation_detail', pk=pk)

    if request.method == 'POST':
        name = accommodation.name
        accommodation.delete()
        messages.success(request, f'Accommodation "{name}" has been deleted successfully.')
        return redirect('bookings:accommodation_list')

    return render(request, 'bookings/accommodation_confirm_delete.html', {'accommodation': accommodation})


@login_required
def book_accommodation(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.accommodation = accommodation

            # Calculate total amount
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            days = (check_out - check_in).days
            booking.total_amount = accommodation.price_per_night * days * booking.number_of_guests

            booking.save()
            messages.success(request, 'Booking successful! Please complete the payment.')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        # Set default values for the form
        tomorrow = datetime.now() + timedelta(days=1)
        day_after_tomorrow = tomorrow + timedelta(days=1)
        form = BookingForm(initial={
            'check_in_date': tomorrow.strftime('%Y-%m-%d'),
            'check_out_date': day_after_tomorrow.strftime('%Y-%m-%d'),
            'number_of_guests': 1,
        })

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'accommodation': accommodation
    })


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Ensure user can only see their own bookings unless they're staff
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('bookings:my_bookings')

    # Calculate stay duration
    stay_duration = (booking.check_out_date - booking.check_in_date).days

    context = {
        'booking': booking,
        'stay_duration': stay_duration,
        'can_cancel': booking.booking_status == 'pending' or booking.booking_status == 'confirmed',
        'can_review': booking.booking_status == 'completed' and not AccommodationReview.objects.filter(
            accommodation=booking.accommodation,
            user=request.user
        ).exists()
    }

    return render(request, 'bookings/booking_detail.html', context)


@login_required
def my_bookings(request):
    # Get all bookings for the current user
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        bookings = bookings.filter(booking_status=status_filter)

    context = {
        'bookings': bookings,
        'status_options': Booking.BOOKING_STATUS,
        'current_status': status_filter or 'all'
    }

    return render(request, 'bookings/my_bookings.html', context)


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Ensure user can only cancel their own bookings
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('bookings:my_bookings')

    # Only pending or confirmed bookings can be cancelled
    if booking.booking_status not in ['pending', 'confirmed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:booking_detail', pk=booking.pk)

    if request.method == 'POST':
        booking.booking_status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled successfully.')

        # If payment was made, handle refund process or notification
        if booking.payment_status == 'paid':
            booking.payment_status = 'refunded'
            booking.save()
            # You could trigger refund notification here

        return redirect('bookings:my_bookings')

    return render(request, 'bookings/booking_cancel.html', {'booking': booking})