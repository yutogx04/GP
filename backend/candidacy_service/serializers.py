from rest_framework import serializers
from .models import Candidacy, CandidacyStatus
from django.contrib.auth import get_user_model
from internship_offer_service.serializers import OfferListSerializer

User = get_user_model()

class CandidacyCreateSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Candidacy
        fields = ("id", "offer", "attachment")

    def validate(self, data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        user = request.user
        # simple eligibility checks; adjust as needed
        if not getattr(user, "email_verified", False):
            raise serializers.ValidationError("Verify your email before applying.")
        if not getattr(user, "is_profile_complete", False):
            raise serializers.ValidationError("Complete your profile before applying.")
        # ensure offer exists and is published
        offer = data.get("offer")
        from internship_offer_service.models import AnnouncementStatus
        if offer.status != AnnouncementStatus.PUBLISHED:
            raise serializers.ValidationError("Cannot apply to an unpublished offer.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        # capture snapshot of minimal user info
        snapshot = {
            "email": user.email,
            "first_name": getattr(user, "first_name", ""),
            "last_name": getattr(user, "last_name", ""),
        }
        validated_data["student"] = user
        validated_data["student_snapshot"] = snapshot
        return super().create(validated_data)

class CandidacyListSerializer(serializers.ModelSerializer):
    offer = OfferListSerializer(read_only=True)

    class Meta:
        model = Candidacy
        fields = ("id", "offer", "applied_at", "status", "motive_rejection", "attachment", "student_snapshot")
class CandidacyDetailSerializer(serializers.ModelSerializer):
    offer = OfferListSerializer(read_only=True)

    class Meta:
        model = Candidacy
        fields = ("id", "offer", "applied_at", "status", "motive_rejection", "attachment", "student_snapshot")