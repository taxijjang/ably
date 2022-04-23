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
    nickname = models.CharField(
        max_length=10,
    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "nickname", "password"]

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
