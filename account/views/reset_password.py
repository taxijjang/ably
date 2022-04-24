from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from ..serializers import ResetPasswordSerializer

User = get_user_model()


class PasswordResetCreateView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["patch"]

    def get_object(self):
        user = get_object_or_404(
            User,
            email=self.request.data.get("email"),
            phone_number=self.request.data.get("phone_number"),
        )
        return user

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
    def patch(self, request):
        serializer = ResetPasswordSerializer(
            instance=self.get_object(), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "비밀번호 재 설정 완료."})
        return Response(
            data={"message": "비밀번호 재 설정 실패"}, status=status.HTTP_400_BAD_REQUEST
        )
