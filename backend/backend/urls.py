from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("auth_service.urls")),
    path("profiles/", include("user_profile_service.urls")),
    path("establishments/", include("establishment_service.urls")),
    path("students/", include("student_service.urls")),
    path("offers/", include("internship_offer_service.urls")),
    path("candidacies/", include("candidacy_service.urls")),
    path("internships/", include("internship_service.urls")),
    path("evaluations/", include("evaluation_service.urls")),
    path("files/", include("student_service.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)