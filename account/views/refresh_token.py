from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_spectacular.utils import extend_schema


class RefreshTokenView(TokenViewBase):
    serializer_class = TokenRefreshSerializer

    @extend_schema(
        tags=["계정"],
        summary="access token 갱신 하는 API",
        description="""refresh token을 이용하여 access token 갱신\n
        """,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
