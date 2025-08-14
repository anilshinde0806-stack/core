from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Service


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


SERVICE_CHOICES = [
    ('haircut', 'Haircut'),
    ('shave', 'Shave'),
    ('facial', 'Facial'),
    ('spa', 'Spa'),
    ('hair_color', 'Hair Color'),
    ('other', 'Other'),
]

class BookingForm(forms.ModelForm):
        class Meta:
            model = Booking
            fields = ['name', 'email', 'phone', 'service', 'appointment_date', 'appointment_time']
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
                'service': forms.Select(attrs={'class': 'form-control'}),
                'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
                }

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['service'].queryset = Service.objects.all()
