from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('auth_service.urls')),
    path('profiles/', include('user_profile_service.urls')),
    path('establishments/', include('establishment_service.urls')),
    path('students/', include('student_service.urls')),
    path('offers/', include('internship_offer_service.urls')),
    path('candidacies/', include('candidacy_service.urls')),
    path('internships/', include('internship_service.urls')),
    path('evaluations/', include('evaluation_service.urls')),
    path('files/', include('file_storage_service.urls')),
]
