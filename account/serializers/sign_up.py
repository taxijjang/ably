from django.contrib.auth import get_user_model

from rest_framework import serializers

from sms.models import AuthSMS
from ..exceptions import SMSAuthIsExpiredException, PasswordIsNotValidException

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    verify_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "verify_password",
            "name",
            "nickname",
            "phone_number",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_phone_number(self, phone_number):
        if not AuthSMS.is_valid_sms_auth(
            phone_number=phone_number, type=AuthSMS.SIGN_UP
        ):
            raise SMSAuthIsExpiredException()
        return phone_number

    def validate(self, attrs):
        password = attrs.get("password")
        verify_password = attrs.pop("verify_password")
        if password != verify_password:
            raise PasswordIsNotValidException()
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
