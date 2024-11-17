from celery import shared_task
from django.core.mail import send_mail
from proj.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_order_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
