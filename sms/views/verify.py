from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from ..serializers import SMSVerifySerializer


class SMSVerifyView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="SMS를 인증하는 API",
        description="""SMS를 인증하는 API
               
        - sms 인증 유효기간은 발송 후 5분입니다.
        """,
        request=SMSVerifySerializer,
        responses={
            200: OpenApiResponse(
                response=dict,
                description="SMS 인증 완료",
                examples=[
                    OpenApiExample(
                        response_only=True,
                        name="성공",
                        value={"message": "인증 완료되었습니다."},
                    )
                ],
            ),
            400: OpenApiResponse(
                response=dict,
                description="SMS 인증 실패",
                examples=[
                    OpenApiExample(
                        response_only=True,
                        name="실패",
                        value={"인증 실패했습니다."},
                    ),
                ],
            ),
        },
    )
    def post(self, request):
        serializer = SMSVerifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "인증 완료되었습니다."})
        return Response(
            data={"message": "인증 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
