from rest_framework import viewsets
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from .models import Stage
from .serializers import StageSerializer
from django.shortcuts import get_object_or_404
from auth_service.permissions import IsEncadrant, IsStudent, IsHospitalAdmin
from candidacy_service.models import Candidacy

class CreateStageView(generics.CreateAPIView):
    serializer_class = StageSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdmin]  # only hospital admins / faculty may create assignments

    def get_serializer(self, *args, **kwargs):
        # set queryset for candidacy field to avoid circular import at module import time
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        # ensure candidacy exists and is not already assigned
        candidacy = serializer.validated_data["candidacy"]
        if hasattr(candidacy, "stage"):
            raise serializers.ValidationError("This candidacy is already assigned to a stage.")
        stage = serializer.save()
        candidacy.status = "assigned"
        candidacy.save(update_fields=["status"])
        return stage

class StudentStagesListView(generics.ListAPIView):
    serializer_class = StageSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Stage.objects.filter(candidacy__student=self.request.user)

class StageDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = StageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # encadrant sees supervised; student sees own; hospital admin sees all
        if getattr(user, "role", None) == "encadrant":
            return Stage.objects.filter(medecin=user)
        if getattr(user, "role", None) == "student":
            return Stage.objects.filter(candidacy__student=user)
        if getattr(user, "role", None) == "hospital_admin":
            return Stage.objects.all()
        return Stage.objects.none()

from rest_framework.decorators import action, api_view
from rest_framework.views import APIView

class FinishStageView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEncadrant]

    def post(self, request, pk):
        stage = get_object_or_404(Stage, pk=pk, medecin=request.user)
        stage.mark_finished()
        return Response({"detail": "Stage marked as finished."})
    
class CancelStageView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHospitalAdmin]

    def post(self, request, pk):
        stage = get_object_or_404(Stage, pk=pk)
        stage.mark_cancelled()
        return Response({"detail": "Stage marked as cancelled."})