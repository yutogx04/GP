from rest_framework import serializers
from backend.backend.models import Doyen


class DoyenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doyen
        fields = '__all__'
