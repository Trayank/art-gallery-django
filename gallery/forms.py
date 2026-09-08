from django import forms
from .models import CommissionRequest, ContactMessage, ArtClass

class CommissionRequestForm(forms.ModelForm):
    STYLE_CHOICES = [
        ('Oil Painting', 'Oil Painting on Canvas'),
        ('Acrylic Art', 'Acrylic Contemporary'),
        ('Watercolor', 'Watercolor Illustration'),
        ('Digital Portrait', 'Digital Fine Art Portrait'),
        ('Mixed Media', 'Mixed Media & Collage'),
        ('Sculpture', 'Sculpture & 3D Artwork'),
    ]

    BUDGET_CHOICES = [
        ('Rs 5,000 - Rs 15,000', 'Rs 5,000 - Rs 15,000 (Small Canvas / Sketch)'),
        ('Rs 15,000 - Rs 35,000', 'Rs 15,000 - Rs 35,000 (Medium Canvas)'),
        ('Rs 35,000 - Rs 75,000', 'Rs 35,000 - Rs 75,000 (Large Statement Piece)'),
        ('Rs 75,000+', 'Rs 75,000+ (Gallery / Mural Installation)'),
    ]

    style = forms.ChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    budget = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    deadline = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-lg'
        })
    )

    class Meta:
        model = CommissionRequest
        fields = ['client_name', 'email', 'phone', 'style', 'budget', 'deadline', 'reference_image', 'description']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Eleanor Vance'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'eleanor@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '+1 (555) 234-5678'
            }),
            'reference_image': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 5,
                'placeholder': 'Describe your vision, preferred colors, dimensions, room setting, and any special requests...'
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'your.email@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Inquiry regarding artwork, exhibition, or press'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 5,
                'placeholder': 'How can we help you?'
            }),
        }


class SeatReservationForm(forms.Form):
    class_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    seats_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 10
        })
    )
