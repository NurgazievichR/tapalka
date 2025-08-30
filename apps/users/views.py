from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import AuthInitDataSerializer
from .service import verify_init_data
from .models import User


class TelegramAuthView(GenericAPIView):
    serializer_class = AuthInitDataSerializer  

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            parsed = verify_init_data(serializer.validated_data["init_data"])
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
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )
