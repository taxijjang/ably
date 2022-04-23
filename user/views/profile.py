from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from ..serializers import UserProfileDetailUpdateSerializer
from ..permissions import IsAuthor

User = get_user_model()


class UserProfileDetailUpdateView(APIView):
    permission_classes = [IsAuthor]
    http_method_names = ["get", "patch"]

    def get_object(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        self.check_object_permissions(self.request, user)
        return user

    @extend_schema(
        tags=["유저"],
        summary="인증된 유저 정보 확인하는 API",
        description="""인증된 유저 정보 확인\n
        jwt 토큰으로 인증된 유저의 정보를 조회한다.
        """,
        responses=UserProfileDetailUpdateSerializer,
    )
    def get(self, request):
        serializer = UserProfileDetailUpdateSerializer(instance=self.request.user)
        return Response(data=serializer.data)

    @extend_schema(
        tags=["유저"],
        summary="인증된 유저의 정보 수정하는 API",
        description="""인증된 유저의 정보를 수정\n
        jwt 토큰으로 인증된 유저의 정보를 수정한다. (nickname, name만 수정 가능)
        """,
        request=UserProfileDetailUpdateSerializer,
        responses=UserProfileDetailUpdateSerializer,
    )
    def patch(self, request):
        user = self.get_object()
        serializer = UserProfileDetailUpdateSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            serializer = UserProfileDetailUpdateSerializer(instance=user)
            return Response(data=serializer.data)
