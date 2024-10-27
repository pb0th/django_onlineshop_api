import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_reset_password_otp(email, otp):
    """Send the OTP to the user's email."""
    subject = "Your Password Reset OTP"
    message = f"Your OTP for resetting the password is {otp}. It is valid for 10 minutes."
    from_email = "noreply.mrbs@gmail.com"

    send_mail(subject, message, from_email, [email])
