from django.db import models

class Booking(models.Model):
    SERVICE_CHOICES = [
        ('haircut', 'Haircut'),
        ('shave', 'Shave'),
        ('facial', 'Facial'),
        ('spa', 'Spa'),
        ('hair_color', 'Hair Color'),
        ('other', 'Other'),
    ]

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

# Create your models here.
