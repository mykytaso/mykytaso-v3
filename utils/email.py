import logging
from pathlib import Path

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class MailgunError(Exception):
    """Custom exception for Mailgun API errors."""


def send_mailgun_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str | None = None,
) -> bool:
    """
    Send email via Mailgun API.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        text_content: Plain text email body (optional)

    Returns:
        bool: True if email sent successfully, False otherwise

    Raises:
        MailgunError: If Mailgun API returns error response
    """
    try:
        response = requests.post(
            f"{settings.MAILGUN_API_URL}/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "text": text_content or "",
            },
            timeout=10,
        )

        if response.status_code == 200:
            logger.info(f"Email sent successfully to {to_email}")
            return True
        error_msg = f"Mailgun API error: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise MailgunError(error_msg)

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error sending email to {to_email}: {e}")
        raise MailgunError(f"Failed to send email: {e}") from e


def send_verification_email(user, verification_url: str, to_email: str | None = None) -> bool:
    """
    Send email verification message to user.

    Args:
        user: User instance
        verification_url: Full URL with verification token
        to_email: Optional email to send to (defaults to user.email)

    Returns:
        bool: True if sent successfully
    """
    current_dir = Path(__file__).parent
    html_template_path = current_dir / "email_templates" / "verification_email.html"
    text_template_path = current_dir / "email_templates" / "verification_email.txt"

    subject = "Verify Your Email Address"

    # Load templates and substitute variables
    html_content = html_template_path.read_text(encoding="utf-8").format(
        username=user.username,
        verification_url=verification_url,
    )

    text_content = text_template_path.read_text(encoding="utf-8").format(
        username=user.username,
        verification_url=verification_url,
    )

    return send_mailgun_email(
        to_email=to_email or user.email,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )


def send_password_reset_email(user, reset_url: str) -> bool:
    """
    Send password reset email to user.

    Args:
        user: User instance
        reset_url: Full URL with password reset token

    Returns:
        bool: True if sent successfully
    """
    current_dir = Path(__file__).parent
    html_template_path = current_dir / "email_templates" / "password_reset_email.html"
    text_template_path = current_dir / "email_templates" / "password_reset_email.txt"

    subject = "Reset Your Password"

    # Load templates and substitute variables
    html_content = html_template_path.read_text(encoding="utf-8").format(
        username=user.username,
        reset_url=reset_url,
    )

    text_content = text_template_path.read_text(encoding="utf-8").format(
        username=user.username,
        reset_url=reset_url,
    )

    return send_mailgun_email(
        to_email=user.email,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )
