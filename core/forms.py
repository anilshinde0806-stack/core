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


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':3}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['phone'].initial = self.instance.profile.phone
            self.fields['address'].initial = self.instance.profile.address

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile
        profile.phone = self.cleaned_data['phone']
        profile.address = self.cleaned_data['address']
        if commit:
            profile.save()
        return user
