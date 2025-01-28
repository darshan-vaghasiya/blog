from rest_framework import status, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import RegistrationSerializer
from .tasks import send_welcome_email


class RegistrationViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        send_welcome_email.delay(instance.id)
        return Response(status=status.HTTP_201_CREATED, data=self.get_serializer(instance).data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh', None)

            if not refresh_token:
                return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

            # Decode the refresh token
            token = RefreshToken(refresh_token)

            # Blacklist the refresh token
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
