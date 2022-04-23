from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from ..serializers import ResetPasswordSerializer

User = get_user_model()


class PasswordResetCreateView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["계정"],
        summary="비밀번호 재 설정하는 API",
        description="""인증된 유저 비밀번호 재 설정\n
        
        """,
        request=ResetPasswordSerializer,
        responses={
            201: OpenApiResponse(
                response=dict,
                description="비밀번호 재 설정 완료",
                examples=[
                    OpenApiExample(
                        "성공",
                        value={"message": "비밀번호 재 설정 완료."},
                    )
                ],
            ),
            400: OpenApiResponse(
                response=dict,
                description="SMS 발송 실패",
                examples=[
                    OpenApiExample(
                        "실패",
                        value={"message": "발송 실패입니다."},
                    )
                ],
            ),
        },
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={"message": "비밀번호 재 설정 완료."})
        return Response(
            data={"message": "비밀번호 재 설정 실패"}, status=status.HTTP_400_BAD_REQUEST
        )
