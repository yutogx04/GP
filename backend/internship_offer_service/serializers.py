from rest_framework import serializers
from .models import Establishment, ServiceHospitalier, Offer

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ("id", "name", "address", "city", "phone", "contact_email")

class ServiceHospitalierSerializer(serializers.ModelSerializer):
    establishment = EstablishmentSerializer(read_only=True)
    establishment_id = serializers.PrimaryKeyRelatedField(
        queryset=Establishment.objects.all(), source="establishment", write_only=True
    )

    class Meta:
        model = ServiceHospitalier
        fields = ("id", "establishment", "establishment_id", "name", "description", "capacite_accueil")

class OfferListSerializer(serializers.ModelSerializer):
    establishment = EstablishmentSerializer(read_only=True)
    service = ServiceHospitalierSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ("id", "title", "description", "establishment", "service", "start_date", "end_date", "number_places", "date_publication", "status")

class OfferCreateSerializer(serializers.ModelSerializer):
    establishment_id = serializers.PrimaryKeyRelatedField(queryset=Establishment.objects.all(), source="establishment")
    service_id = serializers.PrimaryKeyRelatedField(queryset=ServiceHospitalier.objects.all(), source="service")

    class Meta:
        model = Offer
        fields = ("id", "establishment_id", "service_id", "title", "description", "start_date", "end_date", "number_places", "status")

    def create(self, validated_data):
        request = self.context.get("request")
        offer = Offer.objects.create(**validated_data)
        if request and request.user:
            offer.created_by = request.user
            offer.save(update_fields=["created_by"])
        return offer
