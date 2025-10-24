from django.contrib import admin
from .models import Event, Theme, EventBooking

admin.site.register(Event)
admin.site.register(Theme)
admin.site.register(EventBooking)
