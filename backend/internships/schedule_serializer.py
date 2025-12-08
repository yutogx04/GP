from rest_framework import serializers
from .models import InternshipOffer, Internship, Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    internship_title = serializers.CharField(source='internship.offer.title', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'internship', 'internship_title', 'title', 'description',
            'event_type', 'date', 'start_time', 'end_time', 'location',
            'reminder_24h', 'reminder_1h', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
