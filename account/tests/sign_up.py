from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from sms.models import AuthSMS
from sms.tests import SMSVerifyTestCase

User = get_user_model()


class AccountSingUpTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_유저_회원가입_성공(self, password="test_password"):
        유저정보 = {
            "email": "gw9122@naver.com",
            "password": password,
            "verify_password": "test_password",
            "name": "test_name",
            "nickname": "nickname",
            "phone_number": "01063110710",
        }
        SMSVerifyTestCase().test_회원가입_문자_메시지_인증_성공(
            phone_number=유저정보.get("phone_number")
        )

        client = APIClient()
        response = client.post(reverse("api:account:sign_up"), data=유저정보)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(
            email=유저정보.get("email"), phone_number=유저정보.get("phone_number")
        )
        self.assertEqual(
            response.json(),
            {
                "id": user.pk,
                "email": 유저정보.get("email"),
                "name": 유저정보.get("name"),
                "nickname": 유저정보.get("nickname"),
                "phone_number": 유저정보.get("phone_number"),
            },
        )
        return user

    def test_비밀번호_검증실패로_회원가입_실패(self):
        유저정보 = {
            "email": "gw9122@naver.com",
            "password": "test_password",
            "verify_password": "test_verify_password",
            "name": "test_name",
            "nickname": "nickname",
            "phone_number": "01063110710",
        }
        SMSVerifyTestCase().test_회원가입_문자_메시지_인증_성공(
            phone_number=유저정보.get("phone_number")
        )

        client = APIClient()
        response = client.post(reverse("api:account:sign_up"), data=유저정보)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_문자인증_하지않고_회원가입_진행시_실패(self):
        유저정보 = {
            "email": "gw9122@naver.com",
            "password": "test_password",
            "verify_password": "test_verify_password",
            "name": "test_name",
            "nickname": "nickname",
            "phone_number": "01063110710",
        }
        client = APIClient()
        response = client.post(reverse("api:account:sign_up"), data=유저정보)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_문자인증_유효시간을_초과했을때_회원가입_실패(self):
        유저정보 = {
            "email": "gw9122@naver.com",
            "password": "test_password",
            "verify_password": "test_verify_password",
            "name": "test_name",
            "nickname": "nickname",
            "phone_number": "01063110710",
        }
        SMSVerifyTestCase().test_회원가입_문자_메시지_인증_성공(
            phone_number=유저정보.get("phone_number")
        )

        # 유효시간 지나도록 시간 추가
        auth_sms = AuthSMS.objects.first()
        auth_sms.verify -= timezone.timedelta(minutes=5)
        auth_sms.save()

        client = APIClient()
        response = client.post(reverse("api:account:sign_up"), data=유저정보)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
