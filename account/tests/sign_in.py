from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .sign_up import AccountSingUpTestCase

User = get_user_model()


class AccountSingInTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_유저_로그인_성공(self):
        test_password = "test_password"
        user = AccountSingUpTestCase().test_유저_회원가입_성공(password=test_password)

        client = APIClient()
        response = client.post(
            reverse("api:account:sign_in"),
            data={"email": user.email, "password": test_password},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 2)
        for key in response.json().keys():
            with self.subTest(state="토큰", token_type=key):
                self.assertIn(key, ["access", "refresh"])

        token_data = response.json()
        return token_data

    def test_유저_정보가_올바르지_않아_로그인_실패(self):
        test_password = "test_password"
        fail_test_password = test_password + "test"
        user = AccountSingUpTestCase().test_유저_회원가입_성공(password=test_password)

        client = APIClient()
        response = client.post(
            reverse("api:account:sign_in"),
            data={"email": user.email, "password": fail_test_password},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
