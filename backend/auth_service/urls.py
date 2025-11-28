from django.urls import path
from .views import RegisterView, VerifyEmailView, MeView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "auth_service"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("me/", MeView.as_view(), name="me"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
