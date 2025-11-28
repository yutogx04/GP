from rest_framework import serializers
from .models import Stage
from candidacy_service.serializers import CandidacyListSerializer
from candidacy_service.models import Candidacy

class StageSerializer(serializers.ModelSerializer):
    candidacy = CandidacyListSerializer(read_only=True)
    candidacy_id = serializers.PrimaryKeyRelatedField(source="candidacy", queryset=Candidacy.objects.all(), write_only=True)  # set in view

    class Meta:
        model = Stage
        fields = ("id", "candidacy", "candidacy_id", "medecin", "start_date", "end_date", "status", "final_report")
        read_only_fields = ("status",)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["candidacy_id"].queryset = Candidacy.objects.all()
        self.fields["candidacy_id"].queryset = Candidacy.objects.all()