from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="회원가입"),
    path("signin/", views.SignInView.as_view(), name="로그인"),
]
