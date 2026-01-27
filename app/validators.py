import re
from rest_framework.serializers import ValidationError


def validate_password_strength(password):
    """
    Validates that the password meets complexity requirements.
    Raises ValidationError if the password is not strong enough.
    """
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one number.')
    if not re.search(r'[\W_]', password):
        raise ValidationError('Password must contain at least one special character.')
