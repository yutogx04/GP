from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EstablishmentViewSet, HospitalServiceViewSet, DoctorViewSet

router = DefaultRouter()
router.register(r'establishments', EstablishmentViewSet, basename='establishment')
router.register(r'services', HospitalServiceViewSet, basename='hospitalservice')
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('', include(router.urls)),
]
