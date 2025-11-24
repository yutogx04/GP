from rest_framework import serializers
from .models import Doyen


class DoyenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doyen
        fields = '__all__'
