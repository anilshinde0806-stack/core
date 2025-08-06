from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'appointment_date', 'appointment_time', 'created_at')
from django.contrib import admin

# Register your models here.
