from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # Normalize the email (lowercasing the domain part) … 
        if not email:
            raise ValueError("User must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    # … any other fields you need …
    username = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField()
    phone = models.IntegerField(null=True)
    address = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)


    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def generateOtp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiry = timezone.now() + timedelta(minutes=10)  # otp valid for 10 min.

        return self.otp
        
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    




class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user.first_name)




