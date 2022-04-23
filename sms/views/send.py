from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from ..serializers import SMSSendSerializer


class SMSSendView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="SMS을 발송하는 API",
        description="""SMS을 발송하는 API
        
        - sms 발송 할때 어떤 이유로 발송하는지 작성해야합니다.
            ex) sign_up, password_reset, ...
        """,
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
