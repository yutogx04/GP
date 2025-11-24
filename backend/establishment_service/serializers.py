from rest_framework import serializers
from backend.backend.models import Establishment, Hospital_service, Doctor


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = '__all__'


class HospitalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital_service
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
