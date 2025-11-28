from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import AssignmentOverride
from .serializers import AssignmentOverrideSerializer
from auth_service.permissions import IsFacultyAdmin

class AssignmentOverrideCreateView(generics.CreateAPIView):
    serializer_class = AssignmentOverrideSerializer
    permission_classes = [permissions.IsAuthenticated, IsFacultyAdmin]

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)
        
class AssignmentOverrideListView(generics.ListAPIView):
    serializer_class = AssignmentOverrideSerializer
    permission_classes = [permissions.IsAuthenticated, IsFacultyAdmin]

    def get_queryset(self):
        return AssignmentOverride.objects.all().order_by("-created_at")