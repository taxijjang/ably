from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework import serializers

from sms.models import AuthSMS
from ..exceptions import SMSAuthIsExpiredException, PasswordIsNotValidException

User = get_user_model()


class ResetPasswordSerializer(serializers.ModelSerializer):
    verify_password = serializers.CharField(write_only=True, help_text="비밀번호 검증")

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "password", "verify_password")
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        phone_number = attrs.get("phone_number")
        if not AuthSMS.is_valid_sms_auth(
            phone_number=phone_number, type=AuthSMS.RESET_PASSWORD
        ):
            raise SMSAuthIsExpiredException()

        try:
            User.objects.get(email=email, phone_number=phone_number)
        except User.DoesNotExist:
            raise exceptions.ValidationError("계정 정보가 일치하지 않습니다.")

        password = attrs.get("password")
        verify_password = attrs.pop("verify_password")
        if password != verify_password:
            raise PasswordIsNotValidException()
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        instance.password = password
        instance.save()
        return instance
