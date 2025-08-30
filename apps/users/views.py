# apps/users/views.py
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AuthInitDataSerializer
from .service import verify_init_data

User = get_user_model()

class TelegramAuthView(APIView):
    def post(self, request):
        init_data = AuthInitDataSerializer(data=request.data)
        init_data.is_valid(raise_exception=True)

        try:
            parsed = verify_init_data(init_data.validated_data["init_data"])
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_data = parsed["user"]
        tg_id = user_data.get("id")
        if not tg_id:
            return Response({"detail": "Missing telegram id"}, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(
            telegram_id=tg_id,
            defaults={
                "username": user_data.get("username"),
                "first_name": user_data.get("first_name") or "",
                "last_name": user_data.get("last_name") or "",
            },
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)
