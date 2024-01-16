from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from core import settings
from todo.models import ToDo


@shared_task
def check_todo_deadline():
    """
    Celery task to check todo deadlines and send email notifications
    """
    one_hour_from_now = timezone.now() + timedelta(hours=1)
    todos_to_notify = ToDo.objects.filter(
        deadline__lte=one_hour_from_now, active=True, notified=False
    )

    for todo in todos_to_notify:
        subject = f"Reminder: Deadline for '{todo.title}'"
        message = (
            f"Dear {todo.owner.username},"
            f"\n\nThis is a reminder that the deadline for your todo'{todo.title}'"
            f" is approaching. Please make sure to complete it on time."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[todo.owner.email],
            fail_silently=False,
        )
        todo.notified = True
        todo.save()
