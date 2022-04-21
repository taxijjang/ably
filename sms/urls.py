from django.urls import path

from . import views

urlpatterns = [
    path("send/", views.SMSSendView.as_view(), name="sms_send"),
    path("verify/", views.SMSVerifyView.as_view(), name="sms_verify"),
]
