from random import randint
from django.core.mail import send_mail

def generate_otp():
    """
    Generate a random OTP (One-Time Password) of 6 digits.
    """
    return str(randint(100000, 999999))


def send_otp(email, otp_code):
    """
    Send an email containing the OTP code to the specified email address.
    """
    subject = 'OTP Verification Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = 'electronshop409@gmail.com'  # Update with your email address or use a custom email sender
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)