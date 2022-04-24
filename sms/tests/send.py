from unittest.mock import patch, MagicMock

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import AuthSMS
from ..serializers import SMSSendSerializer


class MockResponse:
    def __init__(self):
        self.status_code = status.HTTP_202_ACCEPTED

    def json(self):
        return {"message": "발송 완료되었습니다."}


class SMSSendTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    @patch("sms.utils.requests")
    def test_회원_가입전_문자_메시지_발송(self, mocked_requests=None):
        client = APIClient()
        mocked_requests.post = MagicMock(return_value=MockResponse())
        mocked_requests.status_code = status.HTTP_201_CREATED
        data = {
            "phone_number": "01063110710",
            "type": AuthSMS.SIGN_UP,
        }
        response = client.post(reverse("api:sms:sms_send"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "발송 완료되었습니다."})

        auth_sms = AuthSMS.objects.filter(
            phone_number=data.get("phone_number"), type=data.get("type")
        ).first()
        self.assertEqual(AuthSMS.objects.count(), 1)
        self.assertEqual(auth_sms.phone_number, data.get("phone_number"))
        self.assertEqual(auth_sms.type, data.get("type"))

        return auth_sms

    @patch("sms.utils.requests")
    def test_비밀번호_재_설정전_문자_메시지_발송(self, mocked_requests=None):
        client = APIClient()
        mocked_requests.post = MagicMock(return_value=MockResponse())
        mocked_requests.status_code = status.HTTP_201_CREATED
        data = {
            "phone_number": "01063110710",
            "type": AuthSMS.RESET_PASSWORD,
        }
        response = client.post(reverse("api:sms:sms_send"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "발송 완료되었습니다."})

        auth_sms = AuthSMS.objects.filter(
            phone_number=data.get("phone_number"), type=data.get("type")
        ).first()
        self.assertEqual(AuthSMS.objects.count(), 1)
        self.assertEqual(auth_sms.phone_number, data.get("phone_number"))
        self.assertEqual(auth_sms.type, data.get("type"))

        return auth_sms
