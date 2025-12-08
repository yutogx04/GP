from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    available_slots = serializers.ReadOnlyField()
    
    class Meta:
        model = Department
        fields = (
            'id', 'hospital', 'hospital_name', 'name', 'description', 
            'capacity', 'available_slots', 'specialty', 'internal_phone', 
            'email', 'head', 'is_active', 'created_at', 'updated_at'
        )

class DepartmentDetailSerializer(DepartmentSerializer):
    hospital = serializers.SerializerMethodField()
    head_name = serializers.CharField(source='head.full_name', read_only=True)
    
    class Meta(DepartmentSerializer.Meta):
        fields = DepartmentSerializer.Meta.fields + ('head_name',)
    
    def get_hospital(self, obj):
        from hospitals.serializers import HospitalSerializer
        return HospitalSerializer(obj.hospital).data