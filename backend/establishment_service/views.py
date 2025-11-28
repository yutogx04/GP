from rest_framework import generics, permissions
from .models import Establishment, ServiceHospitalier
from .serializers import EstablishmentSerializer, ServiceHospitalierSerializer
from auth_service.permissions import IsHospitalAdmin

class EstablishmentListCreateView(generics.ListCreateAPIView):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdmin]

class EstablishmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdmin]

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = ServiceHospitalier.objects.all()
    serializer_class = ServiceHospitalierSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdmin]

class ServiceDetailView(generics.RetrieveUpdateAPIView):
    queryset = ServiceHospitalier.objects.all()
    serializer_class = ServiceHospitalierSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdmin]
