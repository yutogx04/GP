from rest_framework import serializers
from backend.models import Internship


class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'
