from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User
import uuid

SERVICE_CHOICES = ([
        ('haircut', 'Haircut'),
        ('shave', 'Shave'),
        ('facial', 'Facial'),
        ('spa', 'Spa'),
        ('hair_color', 'Hair Color'),
        ('other', 'Other'),
    ])


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['appointment_date']),
            models.Index(fields=['user']),
        ]

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,  # hides it from admin & forms
        blank=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='core_bookings')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if not self.booking_id:  # Only generate for new records
            self.booking_id = f"BK-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

