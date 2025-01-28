import threading
import logging
from celery import shared_task
from django.conf import settings
from .models import CustomUser
from django.core.mail import send_mail


logger = logging.getLogger("my_custom_logger")


class SendMail:
    def trigger_email(self, subject, message, recipient_email):
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
        except Exception as e:
            logger.error(f"Mail sending error => {e}")


def send_email_in_thread(user_id):
    """
    Function to send the email in a separate thread.
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        subject = "Welcome to the Blog Platform!"
        message = f"Hello {user.username}, welcome to our platform!"
        recipient_email = user.email
        email_service = SendMail()
        email_service.trigger_email(subject, message, recipient_email)
    except CustomUser.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending welcome email for user {user_id}: {e}")


@shared_task
def send_welcome_email(user_id):
    """
    Sends a welcome email to the user after registration, using threading to handle the email sending.
    """
    # Start a new thread to send the email
    threading.Thread(target=send_email_in_thread, args=(user_id,)).start()
