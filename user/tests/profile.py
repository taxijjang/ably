from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from account.tests import AccountSingInTestCase

User = get_user_model()


class UserProfileTestCase(APITestCase):
    def setUp(self) -> None:
        self.password = "1234"
        self.user = User.objects.create_user(
            email="test@email.com",
            name="test",
            nickname="test",
            password=self.password,
            phone_number="01063110710",
        )

    def test_유저_프로필_조회_성공(self):
        token_data = AccountSingInTestCase().test_기존_유저_로그인_성공(
            email=self.user.email,
            password=self.password,
        )
        access_token = token_data.get("access")

        client = APIClient()

        # jwt token 헤더에 추가
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = client.get(reverse("api:user:profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.pk, response.json().get("id"))
        self.assertEqual(self.user.email, response.json().get("email"))
        self.assertEqual(self.user.name, response.json().get("name"))
        self.assertEqual(self.user.nickname, response.json().get("nickname"))
        self.assertEqual(self.user.phone_number, response.json().get("phone_number"))

    def test_유저_프로필_수정_성공(self):
        token_data = AccountSingInTestCase().test_기존_유저_로그인_성공(
            email=self.user.email,
            password=self.password,
        )
        access_token = token_data.get("access")

        data = {
            "name": "new_name",
            "nickname": "new_name",
        }
        client = APIClient()
        # jwt token 헤더에 추가
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = client.patch(reverse("api:user:profile"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.pk, response.json().get("id"))
        self.assertEqual(self.user.email, response.json().get("email"))
        self.assertEqual(data.get("name"), response.json().get("name"))
        self.assertEqual(data.get("nickname"), response.json().get("nickname"))
        self.assertEqual(self.user.phone_number, response.json().get("phone_number"))
