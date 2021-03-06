from django.db import models
from django.utils import timezone

from core.models import BaseTimestampModel


class AuthSMS(BaseTimestampModel):
    SIGN_UP = "sign_up"
    RESET_PASSWORD = "reset_password"
    TYPES_SMS_AUTH_CHOICES = [
        (SIGN_UP, "회원가입"),
        (RESET_PASSWORD, "비밀번호 찾기"),
    ]
    VERIFY_TIME = 5  # 5minute
    phone_number = models.CharField(db_index=True, max_length=11)
    code = models.CharField(db_index=True, max_length=6)
    verify = models.DateTimeField(db_index=True, null=True, blank=True)
    type = models.CharField(max_length=14, choices=TYPES_SMS_AUTH_CHOICES)

    class Meta:
        ordering = ["-pk"]

    @classmethod
    def is_valid_sms_auth(cls, phone_number, type):
        queryset = cls.objects.filter(phone_number=phone_number, type=type)
        queryset = queryset.filter(verify__isnull=False)
        queryset = queryset.filter(
            verify__gte=timezone.now() - timezone.timedelta(minutes=cls.VERIFY_TIME)
        )
        if queryset.exists():
            return True
        return False
