import threading
from django.core.mail import send_mail
from django.conf import settings

def send_custom_email(subject, message, recipient_list, fail_silently=False):
    send_mail(
        subject, message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=fail_silently,
    )

def send_custom_email_async(subject, message, recipient_list, fail_silently=False):
    """Dispatch email send() on a separate thread and return the thread object."""
    thread = threading.Thread(
        target=send_custom_email,
        args=(subject, message, recipient_list, fail_silently),
        daemon=True
    )
    thread.start()
    return thread
