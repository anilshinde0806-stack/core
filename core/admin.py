from django.contrib import admin
from .models import Booking
from .models import Product
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name','user', 'service', 'appointment_date', 'appointment_time', 'created_at')
    list_filter = ('service', 'appointment_date')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)


admin.site.register(Product)


# Register your models here.
