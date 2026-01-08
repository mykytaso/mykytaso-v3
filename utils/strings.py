import secrets


def random_verification_token(length: int = 48):
    """
    Generate a cryptographically secure token for email verification.

    Args:
        length: Number of random bytes (default 48, which encodes to ~64 chars)

    Returns:
        URL-safe base64-encoded token string (~64 characters)
    """
    return secrets.token_urlsafe(length)
