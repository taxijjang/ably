from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignInView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

    @extend_schema(
        tags=["계정"],
        summary="로그인해서 jwt token 획득하는 API",
        description="이메일과 비밀번호를 이용하여 access, refresh token 획득",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
