from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CreateUsers(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        # The username is handled by the model's save() method if not in extra_fields
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.Role.ADMINISTRATOR)

        # These checks are good practice to ensure integrity
        if extra_fields.get('role') is not self.model.Role.ADMINISTRATOR:
            raise ValueError('Superuser must have role of Administrator.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMIN', 'Administrator'
        VENDOR = 'SELLER', 'Vendor'
        CUSTOMER = 'USER', 'Customer'
        
    role = models.CharField(max_length=50, choices=Role.choices, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    objects = CreateUsers()

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = self.email.split('@')[0].lower()
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username