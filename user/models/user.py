from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.models import BaseTimestampModel
from ..managers import UserManager


class User(AbstractBaseUser, BaseTimestampModel):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=10,
    )
    is_active = models.BooleanField(
        default=True,
    )
    phone_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    def __str__(self):
        return self.name
