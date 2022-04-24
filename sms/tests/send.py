from unittest.mock import patch, MagicMock

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import AuthSMS


class MockResponse:
    def __init__(self):
        self.status_code = status.HTTP_202_ACCEPTED

    def json(self):
        return {"message": "발송 완료되었습니다."}


class SMSSendTestCase(APITestCase):
    @patch("sms.utils.requests")
    def test_회원_가입_문자_메시지_발송(self, mocked_requests=None):
        회원가입전_정보 = {
            "phone_number": "01063110710",
            "type": AuthSMS.SIGN_UP,
        }
        client = APIClient()
        mocked_requests.post = MagicMock(return_value=MockResponse())
        mocked_requests.status_code = status.HTTP_201_CREATED
        response = client.post(reverse("api:sms:sms_send"), 회원가입전_정보)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "발송 완료되었습니다."})

        auth_sms = AuthSMS.objects.filter(**회원가입전_정보).first()
        self.assertEqual(AuthSMS.objects.count(), 1)
        self.assertEqual(auth_sms.phone_number, 회원가입전_정보.get("phone_number"))
        self.assertEqual(auth_sms.type, 회원가입전_정보.get("type"))

        return auth_sms

    @patch("sms.utils.requests")
    def test_비밀번호_재_설정_문자_메시지_발송(self, mocked_requests=None):
        비밀번호_재설정_정보 = {
            "phone_number": "01063110710",
            "type": AuthSMS.RESET_PASSWORD,
        }
        client = APIClient()
        mocked_requests.post = MagicMock(return_value=MockResponse())
        mocked_requests.status_code = status.HTTP_201_CREATED
        response = client.post(reverse("api:sms:sms_send"), 비밀번호_재설정_정보)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "발송 완료되었습니다."})

        auth_sms = AuthSMS.objects.filter(**비밀번호_재설정_정보).first()
        self.assertEqual(AuthSMS.objects.count(), 1)
        self.assertEqual(auth_sms.phone_number, 비밀번호_재설정_정보.get("phone_number"))
        self.assertEqual(auth_sms.type, 비밀번호_재설정_정보.get("type"))

        return auth_sms
