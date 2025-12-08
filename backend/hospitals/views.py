from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hospital, HospitalAdmin
from .serializers import HospitalSerializer, HospitalDetailSerializer, HospitalAdminSerializer

class HospitalListView(generics.ListAPIView):
    queryset = Hospital.objects.filter(is_active=True)
    serializer_class = HospitalSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hospital_type', 'city', 'state']
    search_fields = ['name', 'city', 'state']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class HospitalDetailView(generics.RetrieveAPIView):
    queryset = Hospital.objects.filter(is_active=True)
    serializer_class = HospitalDetailSerializer
    permission_classes = [permissions.AllowAny]

class HospitalAdminListView(generics.ListAPIView):
    serializer_class = HospitalAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'hospital_admin':
            return HospitalAdmin.objects.filter(user=user)
        elif user.role in ['faculty_admin', 'encadrant']:
            return HospitalAdmin.objects.filter(is_active=True)
        return HospitalAdmin.objects.none()

class HospitalAdminDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = HospitalAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if user.role == 'hospital_admin':
            return generics.get_object_or_404(HospitalAdmin, user=user)
        return generics.get_object_or_404(HospitalAdmin, id=self.kwargs['pk'])