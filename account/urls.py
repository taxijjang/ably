from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="sign_up"),
    path("signin/", views.SignInView.as_view(), name="sign_in"),
    path("refresh/", views.RefreshTokenView.as_view(), name="token_refresh"),
    path(
        "rest-password", views.PasswordResetCreateView.as_view(), name="rest_password"
    ),
]
