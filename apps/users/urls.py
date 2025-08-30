from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TelegramAuthView

urlpatterns = [
    path("auth/telegram/", TelegramAuthView.as_view(), name="telegram_auth"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]