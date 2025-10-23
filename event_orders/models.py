from django.db import models
from eventusers.models import users
from events.models import Event

# --- Cart model ---
class eventcart(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    EVENT_CART = 0
    EVENT_BOOKED = 1
    EVENT_PROCESSED = 2
    EVENT_DELIVERED = 3
    EVENT_REJECTED = 4
    STATUS_CHOICES = (
        (EVENT_CART, 'In Cart'),
        (EVENT_BOOKED, 'Booked'),
        (EVENT_PROCESSED, 'Processed'),
        (EVENT_DELIVERED, 'Delivered'),
        (EVENT_REJECTED, 'Rejected'),
    )

    owner = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, related_name='orders')
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    event_status = models.IntegerField(choices=STATUS_CHOICES, default=EVENT_CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.owner.name}"


class eventbookeditem(models.Model):
    event = models.ForeignKey(Event, related_name='added_events', on_delete=models.SET_NULL, null=True)
    guestcount = models.IntegerField(default=1)
    owner = models.ForeignKey(eventcart, on_delete=models.CASCADE, related_name='added_events')

    def __str__(self):
        return f"{self.event.title} ({self.guestcount})"
