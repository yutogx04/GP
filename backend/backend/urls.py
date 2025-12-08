from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def health_check(request):
    return JsonResponse({"status": "healthy", "service": "Hospital Internship Platform"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    path('api/users/', include('users.urls')),
    path('api/auth/', include('authentification.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/hospitals/', include('hospitals.urls')),
    path('api/internships/', include('internships.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/evaluations/', include('evaluations.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)