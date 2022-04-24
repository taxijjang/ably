from django.utils import timezone

from rest_framework import serializers, exceptions

from ..models import AuthSMS


class SMSVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthSMS
        fields = [
            "id",
            "phone_number",
            "code",
            "type",
        ]

    def validate_code(self, code):
        if len(code) != 6:
            raise exceptions.ValidationError()
        return code

    def validate(self, attrs):
        VERIFY_LIMIT_TIME = timezone.now() - timezone.timedelta(minutes=5)
        phone_number = attrs.get("phone_number")
        code = attrs.get("code")
        type = attrs.get("type")
        obj = AuthSMS.objects.filter(
            phone_number=phone_number,
            verify__isnull=True,
            type=type,
            created__gte=VERIFY_LIMIT_TIME,
        ).first()
        if not obj:
            raise exceptions.ValidationError("해당 휴대폰 번호에 인증 데이터가 존재하지 않습니다")
        if obj.code != code:
            raise exceptions.ValidationError("인증 번호가 틀립니다")
        return attrs

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        code = validated_data.get("code")
        obj = AuthSMS.objects.filter(phone_number=phone_number, code=code).first()
        obj.verify = timezone.now()
        obj.save()
        return obj
