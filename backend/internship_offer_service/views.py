from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Establishment, ServiceHospitalier, Offer, AnnouncementStatus
from .serializers import EstablishmentSerializer, ServiceHospitalierSerializer, OfferListSerializer, OfferCreateSerializer
from .permissions import IsHospitalAdmin, IsAuthenticatedAndProfileComplete

class OfferListView(generics.ListAPIView):
    serializer_class = OfferListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "service__name", "establishment__name"]
    ordering_fields = ["date_publication", "start_date"]
    queryset = Offer.objects.filter(status=AnnouncementStatus.PUBLISHED)

class OfferDetailView(generics.RetrieveAPIView):
    serializer_class = OfferListSerializer
    permission_classes = [AllowAny]
    queryset = Offer.objects.all()

class OfferCreateView(generics.CreateAPIView):
    serializer_class = OfferCreateSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

class OfferUpdateView(generics.UpdateAPIView):
    serializer_class = OfferCreateSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]
    queryset = Offer.objects.all()

# publish endpoint (hospital admin)
from rest_framework.views import APIView

class OfferPublishView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        offer.publish(by_user=request.user)
        return Response({"detail": "Offer published.", "id": offer.id, "status": offer.status}, status=status.HTTP_200_OK)

# Simple endpoints to manage establishments/services (hospital admins)
class EstablishmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EstablishmentSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]
    queryset = Establishment.objects.all()

class ServiceHospitalierListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceHospitalierSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]
    queryset = ServiceHospitalier.objects.all()
