from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .sign_in import AccountSingInTestCase

User = get_user_model()


class RefreshTokenTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_access_토큰_재발급_성공(self):
        token_data = AccountSingInTestCase().test_유저_로그인_성공()
        refresh_token = {"refresh": token_data.get("refresh")}

        client = APIClient()
        response = client.post(reverse("api:account:token_refresh"), data=refresh_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())

    def test_access_토큰_재발급_실패(self):
        token_data = AccountSingInTestCase().test_유저_로그인_성공()
        refresh_token = {"refresh": token_data.get("refresh")[:-1]}

        client = APIClient()
        response = client.post(reverse("api:account:token_refresh"), data=refresh_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
