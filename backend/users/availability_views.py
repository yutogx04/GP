from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .availability import AvailabilitySlot, UnavailableDate
from rest_framework import serializers

User = get_user_model()

class AvailabilitySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = '__all__'
        read_only_fields = ('supervisor',)

class UnavailableDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnavailableDate
        fields = '__all__'
        read_only_fields = ('supervisor',)

class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AvailabilitySlot.objects.filter(supervisor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(supervisor=self.request.user)

class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AvailabilitySlot.objects.filter(supervisor=self.request.user)

class UnavailableDateListCreateView(generics.ListCreateAPIView):
    serializer_class = UnavailableDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UnavailableDate.objects.filter(supervisor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(supervisor=self.request.user)

class UnavailableDateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UnavailableDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UnavailableDate.objects.filter(supervisor=self.request.user)
