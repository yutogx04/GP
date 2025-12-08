from rest_framework import serializers
from .models import Evaluation, AutoEvaluation


class EvaluationListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='internship.student.user.full_name', read_only=True)
    offer_title = serializers.CharField(source='internship.offer.title', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.full_name', read_only=True)
    mention = serializers.SerializerMethodField()
    
    class Meta:
        model = Evaluation
        fields = [
            'id', 'internship', 'supervisor', 'supervisor_name',
            'student_name', 'offer_title', 'final_grade', 'mention',
            'is_submitted', 'is_validated', 'evaluation_date'
        ]
    
    def get_mention(self, obj):
        return obj.get_mention()


class EvaluationDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='internship.student.user.full_name', read_only=True)
    offer_title = serializers.CharField(source='internship.offer.title', read_only=True)
    hospital_name = serializers.CharField(source='internship.offer.hospital.name', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.full_name', read_only=True)
    mention = serializers.SerializerMethodField()
    
    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['supervisor', 'evaluation_date', 'is_validated', 'validated_by', 'validation_date']
    
    def get_mention(self, obj):
        return obj.get_mention()


class EvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            'internship', 'technical_skills', 'attendance_punctuality',
            'patient_relation', 'teamwork', 'initiative_autonomy',
            'theoretical_knowledge', 'overall_appreciation', 'strengths',
            'areas_for_improvement', 'recommendations', 'suitable_for_next_internship',
            'recommend_for_supervision', 'thesis_opinion', 'supervisor_signature'
        ]
    
    def create(self, validated_data):
        validated_data['supervisor'] = self.context['request'].user
        validated_data['is_submitted'] = True
        evaluation = super().create(validated_data)
        evaluation.calculate_final_grade()
        return evaluation


class AutoEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoEvaluation
        fields = '__all__'
        read_only_fields = ['submission_date']