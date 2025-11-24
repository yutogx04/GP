from rest_framework import serializers
from backend.backend.models import candidacy


class CandidacySerializer(serializers.ModelSerializer):
    class Meta:
        model = candidacy
        fields = '__all__'
