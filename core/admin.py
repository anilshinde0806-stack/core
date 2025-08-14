from django.contrib import admin
from .models import Booking
from .models import Product
from .models import Booking, Service

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name','user', 'service', 'appointment_date', 'appointment_time', 'created_at')
    list_filter = ('service', 'appointment_date')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)


admin.site.register(Product)
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
