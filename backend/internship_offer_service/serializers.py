from rest_framework import serializers
from backend.backend.models import Internship_announcement


class InternshipAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship_announcement
        fields = '__all__'
