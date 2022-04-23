from django.contrib.auth import get_user_model

from rest_framework import serializers

from sms.models import AuthSMS
from ..exceptions import SMSAuthIsExpiredException

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "name", "nickname", "phone_number")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_phone_number(self, phone_number):
        if not AuthSMS.is_valid_sms_auth(phone_number):
            raise SMSAuthIsExpiredException()
        return phone_number

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
