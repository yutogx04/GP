from rest_framework import serializers
from backend.backend.models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
