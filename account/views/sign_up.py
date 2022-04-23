from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from ..serializers import SignUpSerializer

User = get_user_model()


class SignInCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["계정"],
        summary="회원가입하는 API",
        description="5분 이내 문자 메시지가 인증된 유저만 가입이 가능 합니다.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
