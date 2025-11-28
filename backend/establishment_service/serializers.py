from rest_framework import serializers
from .models import Establishment, ServiceHospitalier

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ("id", "name", "address", "city", "phone", "contact_email")

class ServiceHospitalierSerializer(serializers.ModelSerializer):
    establishment = EstablishmentSerializer(read_only=True)
    establishment_id = serializers.PrimaryKeyRelatedField(queryset=Establishment.objects.all(), source="establishment", write_only=True)

    class Meta:
        model = ServiceHospitalier
        fields = ("id", "establishment", "establishment_id", "name", "description", "capacite_accueil")
