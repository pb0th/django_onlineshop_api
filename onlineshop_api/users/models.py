from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    display_name = models.CharField(_('display name'), blank=True, max_length=100)
    phone_number = models.CharField(_("phone number"), max_length=20)
    date_of_birth = models.DateField(_('date of birth'), blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'phone_number', 'date_of_birth']


    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email