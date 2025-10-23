from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from events.models import Event
from .models import eventcart, eventbookeditem


@login_required
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = request.user.customer_profile  # linked users model (OneToOneField)
    cart, created = eventcart.objects.get_or_create(owner=profile, delete_status=eventcart.LIVE)

    guestcount = int(request.POST.get('guestcount', 1))
    item, created = eventbookeditem.objects.get_or_create(owner=cart, event=event)
    item.guestcount = guestcount
    item.save()

    messages.success(request, f"{event.title} added to your cart.")
    return redirect('orderscart')


@login_required
def show_orderscart(request):
    profile = request.user.customer_profile
    cart = eventcart.objects.filter(owner=profile, delete_status=eventcart.LIVE).first()
    items = cart.added_events.select_related('event').all() if cart else []
    return render(request, 'orderscart.html', {'cart_items': items})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(eventbookeditem, id=item_id, owner__owner=request.user.customer_profile)
    item.delete()
    messages.success(request, f"{item.event.title} removed from your cart.")
    return redirect('orderscart')
