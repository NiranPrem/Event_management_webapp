from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from events.models import Event
from .models import eventcart, eventbookeditem
from eventusers.models import users  # import your customer model


# ---------------- Existing Cart Views ---------------- #

@login_required
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # ✅ Safely get or create customer profile for the logged-in user
    profile, created = users.objects.get_or_create(user=request.user, defaults={
        'name': request.user.username,
        'email': request.user.email,
        'address': '',
        'phone': ''
    })

    cart, created = eventcart.objects.get_or_create(owner=profile, delete_status=eventcart.LIVE)

    guestcount = int(request.POST.get('guestcount', 1))
    item, created = eventbookeditem.objects.get_or_create(owner=cart, event=event)
    item.guestcount = guestcount
    item.save()

    messages.success(request, f"{event.title} added to your cart.")
    return redirect('orderscart')


@login_required
def show_orderscart(request):
    # ✅ Ensure profile exists
    profile, created = users.objects.get_or_create(user=request.user, defaults={
        'name': request.user.username,
        'email': request.user.email,
        'address': '',
        'phone': ''
    })

    cart = eventcart.objects.filter(owner=profile, delete_status=eventcart.LIVE).first()
    items = cart.added_events.select_related('event').all() if cart else []
    return render(request, 'orderscart.html', {'cart_items': items})


@login_required
def remove_from_cart(request, item_id):
    # ✅ Ensure profile exists
    profile, created = users.objects.get_or_create(user=request.user, defaults={
        'name': request.user.username,
        'email': request.user.email,
        'address': '',
        'phone': ''
    })

    item = get_object_or_404(eventbookeditem, id=item_id, owner__owner=profile)
    item.delete()
    messages.success(request, f"{item.event.title} removed from your cart.")
    return redirect('orderscart')


# ---------------- New Payment Views ---------------- #

@login_required
def payment_page(request):
    """
    Display payment form to the user.
    """
    # ✅ Ensure profile exists
    profile, created = users.objects.get_or_create(user=request.user, defaults={
        'name': request.user.username,
        'email': request.user.email,
        'address': '',
        'phone': ''
    })

    cart = eventcart.objects.filter(owner=profile, delete_status=eventcart.LIVE).first()
    items = cart.added_events.select_related('event').all() if cart else []

    if not items:
        messages.warning(request, "Your cart is empty! Please add events before proceeding to payment.")
        return redirect('orderscart')

    total_amount = 0
    for item in items:
        total_amount += item.event.price * item.guestcount  # Assuming Event model has 'price' field

    context = {
        'cart_items': items,
        'total_amount': total_amount,
    }
    return render(request, 'payment.html', context)


@login_required
def process_payment(request):
    """
    Simulates payment gateway processing.
    You can later integrate Razorpay, Stripe, etc.
    """
    # ✅ Ensure profile exists
    profile, created = users.objects.get_or_create(user=request.user, defaults={
        'name': request.user.username,
        'email': request.user.email,
        'address': '',
        'phone': ''
    })

    if request.method == 'POST':
        cart = eventcart.objects.filter(owner=profile, delete_status=eventcart.LIVE).first()

        if not cart:
            messages.error(request, "No active cart found!")
            return redirect('orderscart')

        # Simulate payment success
        cart.delete_status = eventcart.DELETED  # Mark cart as completed
        cart.save()

        # Optionally mark events as booked
        for item in cart.added_events.all():
            item.status = eventbookeditem.BOOKED  # assuming status field exists
            item.save()

        messages.success(request, "Payment successful! Your events have been booked.")
        return redirect('payment_success')

    return redirect('payment_page')


@login_required
def payment_success(request):
    """
    Display a simple payment success page.
    """
    return render(request, 'payment_success.html')
