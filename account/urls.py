from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignInCreateView.as_view(), name="회원가입"),
]
