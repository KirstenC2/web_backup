# handlers.py

from django.dispatch import receiver
from .signals import payment_received
from django.shortcuts import redirect
from django.shortcuts import redirect
from django.urls import reverse

@receiver(payment_received)
def handle_payment_received(sender, payment_id, **kwargs):
    # Perform actions upon receiving payment
    # For example, you can log the payment, update user records, etc.
    print(payment_id)
    return redirect(reverse('user_homepage'))