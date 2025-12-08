from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Department
from .serializers import DepartmentSerializer, DepartmentDetailSerializer

class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hospital', 'specialty']
    search_fields = ['name', 'description', 'hospital__name', 'specialty']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = Department.objects.filter(is_active=True)
        hospital_id = self.request.query_params.get('hospital_id')
        if hospital_id:
            queryset = queryset.filter(hospital_id=hospital_id)
        return queryset

class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentDetailSerializer
    permission_classes = [permissions.AllowAny]