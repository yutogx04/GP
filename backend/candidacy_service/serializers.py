from rest_framework import serializers
from backend.models import Candidacy


class CandidacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidacy
        fields = '__all__'
