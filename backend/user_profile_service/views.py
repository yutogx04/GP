from rest_framework import generics, permissions, parsers
from .serializers import StudentProfileSerializer, PieceJustificativeSerializer
from .models import StudentProfile, PieceJustificative
from django.shortcuts import get_object_or_404

class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # create profile if not exists
        user = self.request.user
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        return profile

class UploadPieceView(generics.CreateAPIView):
    serializer_class = PieceJustificativeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save()

class ListMyPiecesView(generics.ListAPIView):
    serializer_class = PieceJustificativeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.student_profile
        return PieceJustificative.objects.filter(student=profile).order_by("-date_depot")
