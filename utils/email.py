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


def send_verification_email(user, verification_url: str) -> bool:
    """
    Send email verification message to user.

    Args:
        user: User instance
        verification_url: Full URL with verification token

    Returns:
        bool: True if sent successfully
    """
    current_dir = Path(__file__).parent

    subject = "Verify Your Email Address"

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Welcome to mykytaso!</h2>
            <p>Hi {user.username},</p>
            <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
            <p style="margin: 30px 0;">
                <a href="{verification_url}"
                   style="background-color: #0d6efd; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verify Email Address
                </a>
            </p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{verification_url}</p>
            <p><small>This link will expire in 24 hours.</small></p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 12px;">
                If you didn't create an account, you can safely ignore this email.
            </p>
        </body>
    </html>
    """


    text_content = f"""
    Welcome to mykytaso!

    Hi {user.username},

    Thank you for registering. Please verify your email address by visiting:

    {verification_url}

    This link will expire in 24 hours.

    If you didn't create an account, you can safely ignore this email.
    """

    return send_mailgun_email(
        to_email=user.email,
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
    subject = "Reset Your Password"

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Password Reset Request</h2>
            <p>Hi {user.username},</p>
            <p>You requested to reset your password. Click the button below to set a new password:</p>
            <p style="margin: 30px 0;">
                <a href="{reset_url}"
                   style="background-color: #0d6efd; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Reset Password
                </a>
            </p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{reset_url}</p>
            <p><small>This link will expire in 1 hour.</small></p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 12px;">
                If you didn't request a password reset, you can safely ignore this email.
                Your password will not be changed.
            </p>
        </body>
    </html>
    """

    text_content = f"""
    Password Reset Request

    Hi {user.username},

    You requested to reset your password. Visit the link below to set a new password:

    {reset_url}

    This link will expire in 1 hour.

    If you didn't request a password reset, you can safely ignore this email.
    Your password will not be changed.
    """

    return send_mailgun_email(
        to_email=user.email,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )
