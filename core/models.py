from django.contrib.auth.models import User
from django.db import models
SERVICE_CHOICES = ([
        ('haircut', 'Haircut'),
        ('shave', 'Shave'),
        ('facial', 'Facial'),
        ('spa', 'Spa'),
        ('hair_color', 'Hair Color'),
        ('other', 'Other'),
    ])
class Booking(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['appointment_date']),
            models.Index(fields=['user']),
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service} on {self.appointment_date}"

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
