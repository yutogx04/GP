from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

def health(request):
    from django.http import JsonResponse
    return JsonResponse({"status": "ok"})

def home(request):
    from django.http import HttpResponse
    return HttpResponse("Welcome to the GP Backend!")

urlpatterns = [
    path('', home),
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/auth/", include("auth_service.urls", namespace="auth_service")),
    path("api/profile/", include("user_profile_service.urls", namespace="user_profile_service")),
    path("api/doyen/", include("doyen_service.urls", namespace="doyen_service")),
    path("api/establishment/", include("establishment_service.urls", namespace="establishment_service")),
    path("api/student/", include("student_service.urls", namespace="student_service")),
    path("api/internship_offer/", include("internship_offer_service.urls", namespace="internship_offer_service")),
    path("api/candidacy/", include("candidacy_service.urls", namespace="candidacy_service")),
    path("api/internship/", include("internship_service.urls", namespace="internship_service")),
    path("api/evaluation/", include("evaluation_service.urls", namespace="evaluation_service")),
    path("api/file_storage/", include("file_storage_service.urls", namespace="file_storage_service")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)