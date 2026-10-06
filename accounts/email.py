import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_welcome_email(user):
    """Send a welcome email without preventing account creation."""
    try:
        send_mail(
            subject="Welcome to Commonplace",
            message=(
                f"Hi {user.name or user.username},\n\n"
                "Welcome to Commonplace, a quieter corner for ideas worth keeping.\n\n"
                "Your account is ready. We look forward to reading what you share.\n\n"
                "The Commonplace team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except (OSError, SMTPException):
        logger.exception("Welcome email could not be sent to %s.", user.email)
