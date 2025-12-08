from rest_framework import serializers
from .models import Application, ApplicationDocument


class ApplicationListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    offer_title = serializers.CharField(source='offer.title', read_only=True)
    offer_hospital_name = serializers.CharField(source='offer.hospital.name', read_only=True)
    offer_department_name = serializers.CharField(source='offer.department.name', read_only=True)
    
    offer = serializers.SerializerMethodField()
    student_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'student', 'student_name', 'student_email',
            'offer', 'offer_title', 'offer_hospital_name', 'offer_department_name',
            'status', 'priority', 'applied_at', 'score', 'student_profile'
        ]
    
    def get_offer(self, obj):
        return {
            'id': obj.offer.id,
            'title': obj.offer.title,
            'hospital_name': obj.offer.hospital.name,
            'department_name': obj.offer.department.name,
            'start_date': obj.offer.start_date,
            'end_date': obj.offer.end_date,
        }
    
    def get_student_profile(self, obj):
        profile = getattr(obj.student, 'student_profile', None)
        if profile:
            return {
                'student_number': profile.student_number,
                'niveau_etude': profile.niveau_etude,
                'specialite': profile.specialite,
                'average_grade': profile.average_grade,
            }
        return None


class ApplicationDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    offer_title = serializers.CharField(source='offer.title', read_only=True)
    documents = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['student', 'applied_at', 'updated_at']
    
    def get_documents(self, obj):
        return ApplicationDocumentSerializer(obj.documents.all(), many=True).data


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['offer', 'motivation_letter', 'priority']
    
    def validate_offer(self, value):
        user = self.context['request'].user
        if Application.objects.filter(student=user, offer=value).exists():
            raise serializers.ValidationError("You have already applied to this offer")
        
        if value.status != 'open':
            raise serializers.ValidationError("This offer is not accepting applications")
        
        return value


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['id', 'name', 'file', 'uploaded_at']
