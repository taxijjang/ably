from rest_framework.exceptions import APIException


class SMSAuthIsExpiredException(APIException):
    status_code = 400
    default_detail = "문자 인증이 완료된 이후에 회원가입이 가능합니다."
    default_code = "MUST_SMS_AUTH"