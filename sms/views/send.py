from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from ..serializers import SMSSendSerializer


class SMSSendView(APIView):
    @extend_schema(
        summary="SMS을 발송하는 API",
        description="SMS을 발송하는 API",
        request=SMSSendSerializer,
        responses={
            201: OpenApiResponse(
                response=dict,
                description="SMS 발송 완료",
                examples=[
                    OpenApiExample(
                        "성공",
                        value={"message": "발송 완료되었습니다."},
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
        serializer = SMSSendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "발송 완료되었습니다."})
        return Response(
            data={"message": "발송 실패입니다."}, status=status.HTTP_400_BAD_REQUEST
        )
