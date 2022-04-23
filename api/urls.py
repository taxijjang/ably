from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "api"

urlpatterns = [
    # jwt token
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 회원가입
    path("account/", include("account.urls")),
    path("sms/", include("sms.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        # YOUR PATTERNS
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="api:schema"),
            name="swagger-ui",
        ),
        path(
            "redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"
        ),
    ]
