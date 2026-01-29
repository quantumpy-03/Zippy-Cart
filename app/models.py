
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.utils.text import slugify

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
        
    email = models.EmailField(verbose_name=_("Email"), unique=True, null=False, blank=False)
    username = models.CharField(verbose_name=_("username"), max_length=150, unique=True, blank=False, null=False)
    is_active = models.BooleanField(verbose_name=_("active"), default=True)
    is_staff = models.BooleanField(verbose_name=_("staff"),default=False)
    date_joined = models.DateTimeField(verbose_name=_("date joined"),auto_now_add=True)

    role = models.CharField(verbose_name=_("User role"), max_length=50, choices=Role.choices)
        
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
    logo = models.ImageField(verbose_name=_("company logo"), upload_to='vendor_logos/', null=True, blank=True)
    company_name = models.CharField(verbose_name=_("Company Name"), max_length=255, unique=True)
    business_registration_number = models.CharField(verbose_name=_("Registration number"), max_length=255)
    gst_id = models.CharField(verbose_name=_("GST number"), max_length=255)
    phone_number = PhoneNumberField(verbose_name=_("Phone number"))
    website = models.URLField(verbose_name=_("Website"), max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

class CustomerProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    user = models.OneToOneField(User, verbose_name=_("Customer"), on_delete=models.CASCADE, primary_key=True, related_name='customer_profile')
    profile_pic = models.ImageField(verbose_name=_("Profile picture"), upload_to='customer_profiles/', null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name=_("Phone number"))
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=10, choices=Gender.choices, blank=True, null=True)

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    user = models.OneToOneField(User,verbose_name=_("User"), primary_key=True, on_delete=models.CASCADE, related_name='addresses')
    contry = models.CharField(verbose_name=_("Country"), max_length=50, null=False, blank=True)
    state = models.CharField(verbose_name=_("State"), max_length=100, null=False, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=100, null=False, blank=True)
    door_number = models.CharField(verbose_name=_("Door number"), max_length=100, null=False, blank=True)
    street = models.CharField(verbose_name=_("Street"), max_length=100, null=False, blank=True)
    pincode = models.CharField(verbose_name=_("Pincode"), max_length=10, null=False, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.contry}"

#  Category model
class ProductCategory(models.Model):
    category_name = models.CharField(verbose_name=_("Category Name"), max_length=255, unique=True)
    category_image = models.ImageField(verbose_name=_("Category Image"), upload_to='category_images/', null=True, blank=True)
    category_description = models.CharField(verbose_name=_("Category Description"), max_length=255)
    slug = models.SlugField(verbose_name=_("Category Slug"), max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name