from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Notification
from .email_templates import EmailTemplate
from .communication_logs import CommunicationLog
from rest_framework import serializers

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ('created_by',)

class CommunicationLogSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.full_name', read_only=True)
    
    class Meta:
        model = CommunicationLog
        fields = '__all__'

class EmailTemplateListCreateView(generics.ListCreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ['faculty_admin', 'hospital_admin']:
            return EmailTemplate.objects.all()
        return EmailTemplate.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ['faculty_admin', 'hospital_admin']:
            return EmailTemplate.objects.all()
        return EmailTemplate.objects.none()

class CommunicationLogListView(generics.ListAPIView):
    serializer_class = CommunicationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role not in ['faculty_admin', 'hospital_admin']:
            return CommunicationLog.objects.none()
            
        queryset = CommunicationLog.objects.all()
        channel = self.request.query_params.get('channel')
        status = self.request.query_params.get('status')
        
        if channel:
            queryset = queryset.filter(channel=channel)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
