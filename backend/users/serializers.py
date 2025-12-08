from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, Document, AcademicHistory, Conversation, Message

User = get_user_model()


class DocumentSerializer(serializers.ModelSerializer):
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = Document
        fields = (
            'id', 'document_type', 'document_type_display', 'name', 'file', 
            'upload_date', 'is_validated', 'remarks', 'validation_date'
        )
        read_only_fields = ('upload_date', 'validation_date')


class AcademicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHistory
        fields = (
            'id', 'academic_year', 'level', 'annual_average', 
            'mention', 'credits_obtained', 'total_credits'
        )


class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    niveau_etude_display = serializers.CharField(source='get_niveau_etude_display', read_only=True)
    specialite_display = serializers.CharField(source='get_specialite_display', read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    academic_history = AcademicHistorySerializer(many=True, read_only=True)
    age = serializers.ReadOnlyField()
    completed_internships = serializers.ReadOnlyField()
    average_evaluations = serializers.ReadOnlyField()
    
    class Meta:
        model = StudentProfile
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name', 'role',
            'student_number', 'niveau_etude', 'niveau_etude_display', 
            'specialite', 'specialite_display', 'faculty', 'university',
            'birth_date', 'birth_place', 'address', 'phone', 'emergency_phone',
            'average_grade', 'academic_year', 'registration_date', 
            'is_active', 'profile_completed', 'preferred_cities', 
            'preferred_specialties', 'age', 'completed_internships', 
            'average_evaluations', 'documents', 'academic_history'
        )


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = (
            'student_number', 'niveau_etude', 'specialite', 'faculty', 
            'university', 'birth_date', 'birth_place', 'address', 
            'phone', 'emergency_phone', 'average_grade', 'academic_year', 
            'preferred_cities', 'preferred_specialties'
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.ReadOnlyField()
    student_profile = StudentProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'is_active', 'date_joined', 'student_profile'
        )
        read_only_fields = ('email', 'date_joined')


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'sender', 'sender_name', 'sender_email', 'content', 'created_at', 'is_read')
        read_only_fields = ('sender', 'created_at')


class ConversationSerializer(serializers.ModelSerializer):
    participants_data = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ('id', 'subject', 'participants', 'participants_data', 'created_at', 'updated_at', 'last_message', 'unread_count')
    
    def get_participants_data(self, obj):
        return [{'id': p.id, 'name': p.full_name, 'email': p.email} for p in obj.participants.all()]
    
    def get_last_message(self, obj):
        msg = obj.last_message
        if msg:
            return {'content': msg.content[:100], 'sender': msg.sender.full_name, 'created_at': msg.created_at}
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.unread_count(request.user)
        return 0