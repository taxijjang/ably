from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from sms.models import AuthSMS
from sms.tests import SMSVerifyTestCase

User = get_user_model()


class ResetPasswordTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = dict(
            email="gw9122@naver.com",
            name="test",
            nickname="test",
            password="1234",
            phone_number="01063110710",
        )
        User.objects.create_user(**self.user_data)

    def test_비밀번호_재설정_성공(self):
        # 먼저 인증을 진행 한 후에 비밀번호 재설정 가능
        비밀번호재설정데이터 = {
            "email": self.user_data.get("email"),
            "phone_number": self.user_data.get("phone_number"),
            "password": "12345",
            "verify_password": "12345",
        }
        SMSVerifyTestCase().test_비밀번호_재설정_문자_메시지_인증_성공(
            phone_number=비밀번호재설정데이터.get("phone_number")
        )

        client = APIClient()
        response = client.patch(reverse("api:account:reset_password"), data=비밀번호재설정데이터)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_인증_유효시간_초과로_비밀번호_재설정_실패(self):
        비밀번호재설정데이터 = {
            "email": self.user_data.get("email"),
            "phone_number": self.user_data.get("phone_number"),
            "password": "12345",
            "verify_password": "12345",
        }
        SMSVerifyTestCase().test_비밀번호_재설정_문자_메시지_인증_성공(비밀번호재설정데이터.get("phone_number"))

        # 유효시간 지나도록 시간 추가
        auth_sms = AuthSMS.objects.filter(type=AuthSMS.RESET_PASSWORD).first()
        auth_sms.verify -= timezone.timedelta(minutes=5)
        auth_sms.save()

        client = APIClient()
        response = client.patch(reverse("api:account:reset_password"), data=비밀번호재설정데이터)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_비밀번호와_검증비밀번호가_달라_실패(self):
        비밀번호재설정데이터 = {
            "email": self.user_data.get("email"),
            "phone_number": self.user_data.get("phone_number"),
            "password": "12345",
            "verify_password": "54321",
        }
        SMSVerifyTestCase().test_비밀번호_재설정_문자_메시지_인증_성공(
            phone_number=비밀번호재설정데이터.get("phone_number")
        )

        client = APIClient()
        response = client.patch(reverse("api:account:reset_password"), data=비밀번호재설정데이터)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_입력한_계정정보가_달라_실패(self):
        비밀번호재설정데이터 = {
            "email": self.user_data.get("email")[:-1],
            "phone_number": self.user_data.get("phone_number"),
            "password": "12345",
            "verify_password": "12345",
        }
        SMSVerifyTestCase().test_비밀번호_재설정_문자_메시지_인증_성공(
            phone_number=비밀번호재설정데이터.get("phone_number")
        )

        client = APIClient()
        response = client.patch(reverse("api:account:reset_password"), data=비밀번호재설정데이터)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
