from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid

from SakiProject import settings



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    api_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # You can add more like 'first_name', 'last_name'

    def __str__(self):
        return f"{self.email} ({'Admin' if self.is_admin else 'User'})"


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth =models.DateField(null=True)

class UserAddress(models.Model):
    user=models.OneToOneField(User,related_name="address",on_delete=models.CASCADE)
    street =models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.street} + " " +{self.city} + " " + {self.pincode}'

class PhoneOTP(models.Model):
    user = models.OneToOneField(User,to_field='id',on_delete=models.CASCADE)
    otp = models.IntegerField(max_length=6,null=True)

class Meta:
    db_table = 'users'
    indexes = [
        models.Index(fields=['is_admin']),
        models.Index(fields=['api_key']),
        models.Index(fields=['username']),
    ]