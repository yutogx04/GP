from rest_framework import serializers
from .models import Evaluation

class EvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ("id", "stage", "note_competences", "note_assiduite", "note_comportement", "commentaire")
        read_only_fields = ("id",)

class EvaluationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = "__all__"
        read_only_fields = ("id", "stage", "medecin", "date_evaluation", "pdf_report")