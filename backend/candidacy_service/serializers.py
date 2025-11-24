from rest_framework import serializers
from .models import candidacy


class CandidacySerializer(serializers.ModelSerializer):
    class Meta:
        model = candidacy
        fields = '__all__'
