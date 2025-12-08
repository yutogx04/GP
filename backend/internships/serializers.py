from rest_framework import serializers
from .models import InternshipOffer, Internship, InternshipJournal


class InternshipOfferListSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    type_display = serializers.CharField(read_only=True)
    minimum_study_level_display = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = InternshipOffer
        fields = [
            'id', 'title', 'description', 'hospital', 'hospital_name',
            'department', 'department_name', 'type', 'type_display',
            'minimum_study_level', 'minimum_study_level_display',
            'start_date', 'end_date', 'application_deadline',
            'slots', 'available_slots', 'is_paid', 'payment_amount',
            'status', 'status_display', 'validation_status', 'is_urgent',
            'created_at'
        ]


class InternshipOfferDetailSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    type_display = serializers.CharField(read_only=True)
    minimum_study_level_display = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = InternshipOffer
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class InternshipOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipOffer
        fields = [
            'title', 'description', 'prerequisites', 'benefits',
            'hospital', 'department', 'type', 'minimum_study_level',
            'start_date', 'end_date', 'application_deadline',
            'slots', 'is_paid', 'payment_amount', 'required_skills', 'is_urgent'
        ]
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['available_slots'] = validated_data.get('slots', 1)
        return super().create(validated_data)


class InternshipSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    offer_title = serializers.CharField(source='offer.title', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.full_name', read_only=True)
    
    class Meta:
        model = Internship
        fields = '__all__'


class InternshipJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipJournal
        fields = '__all__'
