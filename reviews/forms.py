from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import DestinationReview, AccommodationReview, GuideReview, ReviewPhoto


class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience about this destination...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'content': 'Your Review',
            'rating': 'Rating'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('rating', css_class='form-select'),
            Field('content', css_class='form-control'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary')
        )


class AccommodationReviewForm(forms.ModelForm):
    class Meta:
        model = AccommodationReview
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience about this accommodation...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'content': 'Your Review',
            'rating': 'Rating'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('rating', css_class='form-select'),
            Field('content', css_class='form-control'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary')
        )


class GuideReviewForm(forms.ModelForm):
    class Meta:
        model = GuideReview
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this guide...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'content': 'Your Review',
            'rating': 'Rating'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('rating', css_class='form-select'),
            Field('content', css_class='form-control'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary')
        )


class ReviewPhotoForm(forms.ModelForm):
    class Meta:
        model = ReviewPhoto
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional caption for the photo'
            })
        }
