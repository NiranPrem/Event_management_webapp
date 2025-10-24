from django.db import models
from django.contrib.auth.models import User

# Theme Model
class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Event Model
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


# Event Booking Model
class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
