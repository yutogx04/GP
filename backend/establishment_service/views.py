from rest_framework import viewsets
from backend.backend.models import Establishment, Hospital_service, Doctor
from .serializers import EstablishmentSerializer, HospitalServiceSerializer, DoctorSerializer
from .permissions import IsAdminOrReadOnly


class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class HospitalServiceViewSet(viewsets.ModelViewSet):
    queryset = Hospital_service.objects.all()
    serializer_class = HospitalServiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]
