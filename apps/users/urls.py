from django.urls import path
from apps.users.api_endpoints import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView
)

app_name = "users"
urlpatterns = [
    path("user-register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("user-login/", UserLoginAPIView.as_view(), name="user-login"),
    path("user-logout/", UserLogoutAPIView.as_view(), name="user-logout"),
]