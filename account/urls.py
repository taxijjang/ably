from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="회원가입"),
    path("signin/", views.SignInView.as_view(), name="로그인"),
    path("refresh/", TokenRefreshView.as_view(), name="JWT 토큰 갱신"),
]
