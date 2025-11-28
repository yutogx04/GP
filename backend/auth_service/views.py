from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, UserSerializer, CustomTokenObtainPairSerializer
from django.core import signing
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()
SIGNING_SALT = "auth_service_email_salt"
TOKEN_MAX_AGE = 60 * 60 * 24  # 1 day

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        payload = {"user_id": user.pk}
        signed = signing.dumps(payload, salt=SIGNING_SALT)
        verify_url = self.request.build_absolute_uri(reverse("auth_service:verify-email") + f"?token={signed}")
        send_mail(
            subject="Verify your email",
            message=f"Click the link to verify: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({"detail": "token missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = signing.loads(token, salt=SIGNING_SALT, max_age=TOKEN_MAX_AGE)
            uid = data.get("user_id")
            user = User.objects.get(pk=uid)
            user.email_verified = True
            user.is_active = True
            user.save(update_fields=["email_verified", "is_active"])
            return Response({"detail": "email verified"})
        except signing.SignatureExpired:
            return Response({"detail": "token expired"}, status=status.HTTP_400_BAD_REQUEST)
        except signing.BadSignature:
            return Response({"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND)

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
