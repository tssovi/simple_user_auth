from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
        Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
            Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email Is Required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def get_user_details(self, pk, email):
        """
            Get user details for given email.
        """
        try:
            if email:
                data = self.get(email=email)
            else:
                data = self.get(pk=pk)
        except:
            data = []
        return data

    def update_user(self, email, login_attempt, is_locked, locked_at):
        """
            Update and save a User for given email.
        """
        user = self.get(email=email)
        user.login_attempt = login_attempt
        user.is_locked = is_locked
        user.locked_at = locked_at
        user.save()
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    login_attempt = models.PositiveIntegerField(null=False, default=0)
    is_locked = models.BooleanField(null=False, default=False)
    locked_at = models.DateTimeField(null=True)
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email