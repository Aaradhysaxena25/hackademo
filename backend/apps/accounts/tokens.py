"""
Token generation for email verification using Django's signing framework.
"""

from django.core import signing


VERIFICATION_SALT = "email-verification"
VERIFICATION_MAX_AGE = 86400  # 24 hours


def generate_verification_token(user_id: str) -> str:
    """
    Generate a signed email verification token.
    Valid for 24 hours.
    """
    return signing.dumps({"user_id": user_id}, salt=VERIFICATION_SALT)


def verify_token(token: str) -> str | None:
    """
    Verify an email verification token.

    Returns user_id if valid, None if invalid or expired.
    """
    try:
        data = signing.loads(token, salt=VERIFICATION_SALT, max_age=VERIFICATION_MAX_AGE)
        return data.get("user_id")
    except (signing.BadSignature, signing.SignatureExpired):
        return None
