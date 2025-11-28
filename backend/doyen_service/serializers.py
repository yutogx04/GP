from rest_framework import serializers
from .models import AssignmentOverride

class AssignmentOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentOverride
        fields = ("id", "performed_by", "candidacy_id", "note", "created_at")
        read_only_fields = ("performed_by", "created_at")
