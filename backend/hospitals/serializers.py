from rest_framework import serializers
from .models import Hospital, HospitalAdmin

class HospitalSerializer(serializers.ModelSerializer):
    hospital_type_display = serializers.CharField(source='get_hospital_type_display', read_only=True)
    available_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'hospital_type', 'hospital_type_display', 'address', 
            'city', 'state', 'phone', 'email', 'website', 'latitude', 
            'longitude', 'total_capacity', 'current_capacity', 'available_capacity',
            'director', 'registration_number', 'establishment_date', 
            'description', 'is_active', 'created_at', 'updated_at'
        )
    
    def get_available_capacity(self, obj):
        return max(0, obj.total_capacity - obj.current_capacity)

class HospitalDetailSerializer(HospitalSerializer):
    departments = serializers.SerializerMethodField()
    
    class Meta(HospitalSerializer.Meta):
        fields = HospitalSerializer.Meta.fields + ('departments',)
    
    def get_departments(self, obj):
        from departments.serializers import DepartmentSerializer
        return DepartmentSerializer(
            obj.departments.filter(is_active=True), 
            many=True
        ).data

class HospitalAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = HospitalAdmin
        fields = (
            'id', 'user', 'user_email', 'user_name', 'hospital', 
            'hospital_name', 'position', 'phone', 'is_active', 'appointment_date'
        )