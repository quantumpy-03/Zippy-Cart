
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


#  Model Manager & Custom User Model

class CreateUsers(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.Role.ADMINISTRATOR)
        if extra_fields.get('role') is not self.model.Role.ADMINISTRATOR:
            raise ValueError('Superuser must have role of Administrator.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'
        VENDOR = 'VENDOR', 'Vendor'
        CUSTOMER = 'CUSTOMER', 'Customer'
        
    email = models.EmailField(_("Email"), unique=True, null=False, blank=False)
    username = models.CharField(_("username"), max_length=150, unique=True, blank=False, null=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"),default=False)
    date_joined = models.DateTimeField(_("date joined"),auto_now_add=True)

    role = models.CharField(_("User role"), max_length=50, choices=Role.choices)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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


class VendorProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Vendor"), on_delete=models.CASCADE, primary_key=True, related_name='vendor_profile')
    logo = models.ImageField(_("company logo"), upload_to='vendor_logos/', null=True, blank=True)
    company_name = models.CharField(_("Company Name"), max_length=255)
    business_registration_number = models.CharField(_("Registration number"), max_length=255)
    gst_id = models.CharField(_("GST number"), max_length=255)
    phone_number = PhoneNumberField(_("Phone number"))
    website = models.URLField(_("Website"), max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class CustomerProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    user = models.OneToOneField(User, verbose_name=_("Customer"), on_delete=models.CASCADE, primary_key=True, related_name='customer_profile')
    profile_pic = models.ImageField(_("Profile picture"), upload_to='customer_profiles/', null=True, blank=True)
    phone_number = PhoneNumberField(_("Phone number"))
    date_of_birth = models.DateField(_("Date of birth"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=10, choices=Gender.choices, blank=True, null=True)

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def __str__(self):
        return self.user.username
