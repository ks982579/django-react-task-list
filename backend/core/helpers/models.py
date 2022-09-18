"""
Database Models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Custom Manager for our customer user model."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, Save, and return new user."""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # following should hash password to store securely.
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for application."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assigning custom Manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
