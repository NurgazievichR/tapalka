from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TelegramAuthView

urlpatterns = [
    path("/telegram/", TelegramAuthView.as_view(), name="telegram_auth"),
    path("/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]