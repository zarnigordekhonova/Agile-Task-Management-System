from django.core.mail import send_mail
from django.conf import settings


def send_notification_email(subject, message, recipient_list):
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )


