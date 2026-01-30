import re
from rest_framework.serializers import ValidationError

class CustomPasswordStrengthValidator:
    def __init__(self, min_length=8, max_length=16):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        
        if len(password) < self.min_length:
            raise ValidationError(f'Password must be at least {self.min_length} characters.')
        if len(password) > self.max_length:
            raise ValidationError(f'Password must not exceed {self.max_length} characters.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Password must contain at least one special character.')
    
    def get_help_text(self):
        return f'Password must be between {self.min_length} and {self.max_length} characters. It must contain at least one uppercase letter, one lowercase letter, one number, and one special character.'