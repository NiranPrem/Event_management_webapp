from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from events.models import Event
from .models import eventcart, eventbookeditem

# ---------------- Existing Cart Views ---------------- #

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


# ---------------- New Payment Views ---------------- #

@login_required
def payment_page(request):
    """
    Display payment form to the user.
    """
    profile = request.user.customer_profile
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
    if request.method == 'POST':
        profile = request.user.customer_profile
        cart = eventcart.objects.filter(owner=profile, delete_status=eventcart.LIVE).first()

        if not cart:
            messages.error(request, "No active cart found!")
            return redirect('orderscart')

        # Here you can add payment gateway logic or API call
        # For now, simulate payment success
        cart.delete_status = eventcart.DELETED  # Mark cart as completed
        cart.save()

        # Optionally, mark events as booked
        for item in cart.added_events.all():
            item.status = eventbookeditem.BOOKED  # assuming you have a status field
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
