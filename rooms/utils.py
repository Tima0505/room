from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_booking_email(booking):
    subject = f'Бронь подтверждена: {booking.title}'
    message = render_to_string('rooms/email/booking.txt', {'booking': booking})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.user.email], fail_silently=False)