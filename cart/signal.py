from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from user_app.models import User
import json

@receiver(user_logged_in)
def load_cart_from_user(sender, request, user, **kwargs):
    """Load the user's saved cart into the session after login."""
    if user.old_cart:
        request.session['session_key'] = json.loads(user.old_cart)