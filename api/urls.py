from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = "api"

urlpatterns = [
    # SMS 인증
    path("sms/", include("sms.urls")),
    # 회원가입
    path("accounts/", include("account.urls")),
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
