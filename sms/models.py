from django.db import models

from core.models import BaseTimestampModel


class AuthSMS(BaseTimestampModel):
    SIGN_UP = "sign_up"
    TYPES_SMS_AUTH_CHOICES = [
        (SIGN_UP, "sign_up"),
    ]
    phone_number = models.CharField(db_index=True, max_length=11)
    code = models.CharField(db_index=True, max_length=6)
    verify = models.DateTimeField(db_index=True, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPES_SMS_AUTH_CHOICES)

    class Meta:
        ordering = ["-pk"]
