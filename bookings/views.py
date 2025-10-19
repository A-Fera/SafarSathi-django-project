from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q, Avg
from datetime import datetime, timedelta
from .models import Accommodation
from .forms import AccommodationForm
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

    # Allow any authenticated user to review if they haven't already
    user_can_review = False
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = AccommodationReview.objects.filter(
            accommodation=accommodation,
            user=request.user
        ).exists()

        # Any authenticated user can review if they haven't already
        user_can_review = not user_has_reviewed

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
