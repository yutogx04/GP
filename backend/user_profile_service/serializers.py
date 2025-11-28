from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, PieceJustificative

User = get_user_model()

class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = StudentProfile
        fields = ("id", "email", "first_name", "last_name", "numero_etudiant", "niveau_etude", "date_inscription", "contact_phone", "address")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        if user_data:
            user = instance.user
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)
            user.save()
        return super().update(instance, validated_data)

class PieceJustificativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJustificative
        fields = ("id", "type_piece", "nom_fichier", "fichier", "date_depot")
        read_only_fields = ("date_depot",)

    def create(self, validated_data):
        # ensure student is the one uploading
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        student_profile = request.user.student_profile
        validated_data["student"] = student_profile
        # if nom_fichier not set, set from uploaded file
        if not validated_data.get("nom_fichier") and validated_data.get("fichier"):
            validated_data["nom_fichier"] = validated_data["fichier"].name
        return super().create(validated_data)
    
class EncadrantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = StudentProfile
        fields = ("id", "email", "first_name", "last_name", "department", "phone_number")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        if user_data:
            user = instance.user
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)
            user.save()
        return super().update(instance, validated_data)