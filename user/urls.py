from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("profile/", views.UserProfileDetailUpdateView.as_view(), name="유저 프로필 조회 및 수정")
]
