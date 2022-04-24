from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import AuthSMS
from .send import SMSSendTestCase


class MockResponse:
    def __init__(self):
        self.status_code = status.HTTP_202_ACCEPTED

    def json(self):
        return {"message": "발송 완료되었습니다."}


class SMSVerifyTestCase(APITestCase):
    def setUp(self) -> None:
        self.회원가입전정보 = {
            "phone_number": "01063110710",
            "type": AuthSMS.SIGN_UP,
        }
        self.비밀번호재설정정보 = {
            "phone_number": "01063110710",
            "type": AuthSMS.RESET_PASSWORD,
        }

    def fail_code(self, code: int) -> str:
        new_code = (code + 1) % 1000000
        return str(new_code).zfill(6)

    def test_회원가입_문자_메시지_인증_성공(self):
        client = APIClient()
        auth_sms = SMSSendTestCase().test_회원_가입_문자_메시지_발송()

        verify_data = {
            "phone_number": self.회원가입전정보.get("phone_number"),
            "type": self.회원가입전정보.get("type"),
            "code": auth_sms.code,
        }
        response = client.post(reverse("api:sms:sms_verify"), verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "인증 완료되었습니다."})

        auth_sms.refresh_from_db()
        self.assertIsNotNone(auth_sms.verify)

    def test_회원가입_문자_메시지_인증_번호_일치하지않아_실패(self):
        client = APIClient()
        auth_sms = SMSSendTestCase().test_회원_가입_문자_메시지_발송()

        verify_data = {
            "phone_number": self.회원가입전정보.get("phone_number"),
            "type": self.회원가입전정보.get("type"),
            "code": self.fail_code(int(auth_sms.code)),
        }
        response = client.post(reverse("api:sms:sms_verify"), verify_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"message": "인증 실패했습니다."})

        auth_sms.refresh_from_db()
        self.assertIsNone(auth_sms.verify)

    def test_회원가입_문자_메시지_인증_번호_길이가_일치하지않아_실패(self):
        client = APIClient()
        auth_sms = SMSSendTestCase().test_회원_가입_문자_메시지_발송()

        verify_data = {
            "phone_number": self.회원가입전정보.get("phone_number"),
            "type": self.회원가입전정보.get("type"),
            "code": 123,
        }
        response = client.post(reverse("api:sms:sms_verify"), verify_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"message": "인증 실패했습니다."})

        auth_sms.refresh_from_db()
        self.assertIsNone(auth_sms.verify)

    def test_비밀번호_재설정_문자_메시지_인증_성공(self):
        client = APIClient()
        auth_sms = SMSSendTestCase().test_비밀번호_재_설정_문자_메시지_발송()

        verify_data = {
            "phone_number": self.비밀번호재설정정보.get("phone_number"),
            "type": self.비밀번호재설정정보.get("type"),
            "code": auth_sms.code,
        }
        response = client.post(reverse("api:sms:sms_verify"), verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "인증 완료되었습니다."})

        auth_sms.refresh_from_db()
        self.assertIsNotNone(auth_sms.verify)

    def test_비밀번호_재설정_문자_메시지_인증_번호_일치하지않아_실패(self):
        client = APIClient()
        auth_sms = SMSSendTestCase().test_비밀번호_재_설정_문자_메시지_발송()

        verify_data = {
            "phone_number": self.비밀번호재설정정보.get("phone_number"),
            "type": self.비밀번호재설정정보.get("type"),
            "code": self.fail_code(int(auth_sms.code)),
        }
        response = client.post(reverse("api:sms:sms_verify"), verify_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"message": "인증 실패했습니다."})

        auth_sms.refresh_from_db()
        self.assertIsNone(auth_sms.verify)

    def test_비밀번호_재설정_문자_메시지_인증_번호_길이가_일치하지않아_실패(self):
        client = APIClient()
        auth_sms = SMSSendTestCase().test_비밀번호_재_설정_문자_메시지_발송()

        verify_data = {
            "phone_number": self.비밀번호재설정정보.get("phone_number"),
            "type": self.비밀번호재설정정보.get("type"),
            "code": 123,
        }
        response = client.post(reverse("api:sms:sms_verify"), verify_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"message": "인증 실패했습니다."})

        auth_sms.refresh_from_db()
        self.assertIsNone(auth_sms.verify)
