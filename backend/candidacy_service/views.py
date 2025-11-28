from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Candidacy
from .serializers import CandidacyCreateSerializer, CandidacyListSerializer
from .permissions import IsStudent, IsHospitalOrFacultyAdmin
from internship_offer_service.models import Offer

class ApplyToOfferView(generics.CreateAPIView):
    serializer_class = CandidacyCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

class MyCandidaciesListView(generics.ListAPIView):
    serializer_class = CandidacyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Candidacy.objects.filter(student=self.request.user)

class OfferApplicationsListView(generics.ListAPIView):
    serializer_class = CandidacyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalOrFacultyAdmin]

    def get_queryset(self):
        offer_id = self.kwargs.get("offer_pk")
        offer = get_object_or_404(Offer, pk=offer_id)
        # further restrict: hospital admins only for their own establishment offers
        user = self.request.user
        if getattr(user, "role", None) == "hospital_admin":
            # allow only if this hospital_admin belongs to that establishment
            # if you track hospital-admin <-> establishment relation, check it here.
            pass
        return Candidacy.objects.filter(offer=offer)
    
class UpdateCandidacyStatusView(generics.UpdateAPIView):
    serializer_class = CandidacyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsHospitalOrFacultyAdmin]
    queryset = Candidacy.objects.all()

    def update(self, request, *args, **kwargs):
        candidacy = self.get_object()
        new_status = request.data.get("status")
        motive_rejection = request.data.get("motive_rejection", "")

        if new_status not in dict(Candidacy.CandidacyStatus.choices):
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        candidacy.status = new_status
        if new_status == Candidacy.CandidacyStatus.REJECTED:
            candidacy.motive_rejection = motive_rejection
        else:
            candidacy.motive_rejection = ""
        candidacy.save()

        serializer = self.get_serializer(candidacy)
        return Response(serializer.data)