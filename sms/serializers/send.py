import random

from django.utils import timezone

from rest_framework import serializers, exceptions, status

from ..utils import send_sms
from ..models import AuthSMS


class SMSSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthSMS
        fields = [
            "id",
            "phone_number",
            "type",
        ]

    def create(self, validated_data):
        code = random.randint(100000, 1000000)
        phone_number = validated_data.get("phone_number")
        type = validated_data.get("type")
        response = send_sms(phone_number=phone_number, code=code)

        if response.status_code != status.HTTP_202_ACCEPTED:
            raise exceptions.ValidationError("인증번호 발송에 실패 했습니다.")

        obj = AuthSMS.objects.create(phone_number=phone_number, code=code, type=type)
        return obj
