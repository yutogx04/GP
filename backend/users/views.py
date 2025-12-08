from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg
from .models import StudentProfile, Document, AcademicHistory, Conversation, Message
from .serializers import (
    StudentProfileSerializer, StudentProfileUpdateSerializer, 
    DocumentSerializer, AcademicHistorySerializer,
    UserSerializer, ConversationSerializer, MessageSerializer
)

User = get_user_model()


class StudentProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentProfileSerializer
        return StudentProfileUpdateSerializer
    
    def get_object(self):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile


class DocumentUploadView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student_profile=profile)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return get_object_or_404(Document, id=self.kwargs['pk'], student_profile=profile)


class AcademicHistoryView(generics.ListCreateAPIView):
    serializer_class = AcademicHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return profile.academic_history.all()
    
    def perform_create(self, serializer):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        serializer.save(student_profile=profile)


class AcademicHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AcademicHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return get_object_or_404(AcademicHistory, id=self.kwargs['pk'], student_profile=profile)



class HospitalStaffListView(generics.ListAPIView):
    """List supervisors/staff for hospital admin"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'hospital_admin':
            return User.objects.none()
        return User.objects.filter(role='encadrant').annotate(
            assigned_students_count=Count('supervised_internships')
        )


class HospitalStaffCreateView(generics.CreateAPIView):
    """Create a new staff member (hospital admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'hospital_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        data = request.data
        required = ['email', 'first_name', 'last_name', 'password']
        for field in required:
            if not data.get(field):
                return Response({'detail': f'{field} is required'}, status=400)
        
        if User.objects.filter(email=data['email']).exists():
            return Response({'detail': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='encadrant',
            is_active=True,
            email_verified=True,
            force_password_change=True
        )
        
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'message': 'Staff member created successfully'
        }, status=201)


class HospitalStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a staff member (hospital admin only)"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'hospital_admin':
            return User.objects.none()
        return User.objects.filter(role='encadrant')
    
    def update(self, request, *args, **kwargs):
        if request.user.role != 'hospital_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        user = self.get_object()
        data = request.data
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'is_active' in data:
            user.is_active = data['is_active']
        user.save()
        
        return Response(UserSerializer(user).data)
    
    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'hospital_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        user = self.get_object()
        user.delete()
        return Response({'detail': 'Staff member deleted successfully'}, status=204)



class SupervisorStudentListView(generics.ListAPIView):
    """List students assigned to supervisor"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'encadrant':
            return User.objects.none()
        from internships.models import Internship
        student_profile_ids = Internship.objects.filter(
            supervisor=self.request.user,
            status__in=['pending', 'ongoing']
        ).values_list('student_id', flat=True)
        return User.objects.filter(
            student_profile__id__in=student_profile_ids
        ).select_related('student_profile')



class FacultyStudentListView(generics.ListAPIView):
    """List all students for faculty admin"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'faculty_admin':
            return User.objects.none()
        return User.objects.filter(role='student').select_related('student_profile')


class FacultyStudentCreateView(generics.CreateAPIView):
    """Create a new student (faculty admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'faculty_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        data = request.data
        
        required = ['first_name', 'last_name', 'password', 'student_number']
        for field in required:
            if not data.get(field):
                return Response({'detail': f'{field} is required'}, status=400)
        
        email = data.get('email') or f"{data['student_number']}@student.edu"
        
        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Email or matricule already exists'}, status=400)
        
        user = User.objects.create_user(
            email=email,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='student',
            is_active=True,
            email_verified=True,
            force_password_change=True
        )
        
        StudentProfile.objects.create(
            user=user,
            student_number=data['student_number'],
            niveau_etude=data.get('niveau_etude', ''),
            specialite=data.get('specialite', ''),
            faculty=data.get('faculty', ''),
            university=data.get('university', ''),
            phone=data.get('phone', ''),
        )
        
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'student_number': data['student_number'],
            'message': 'Student created successfully'
        }, status=201)


class FacultyStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a student (faculty admin only)"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'faculty_admin':
            return User.objects.none()
        return User.objects.filter(role='student')
    
    def update(self, request, *args, **kwargs):
        if request.user.role != 'faculty_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        user = self.get_object()
        data = request.data
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'is_active' in data:
            user.is_active = data['is_active']
        user.save()
        
        profile = getattr(user, 'student_profile', None)
        if profile:
            for field in ['student_number', 'niveau_etude', 'specialite', 'faculty', 'university', 'phone']:
                if field in data:
                    setattr(profile, field, data[field])
            profile.save()
        
        return Response(UserSerializer(user).data)
    
    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'faculty_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        user = self.get_object()
        user.delete()
        return Response({'detail': 'Student deleted successfully'}, status=204)


class FacultyReportsView(APIView):
    """Generate faculty reports/statistics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'faculty_admin':
            return Response({'detail': 'Not authorized'}, status=403)
        
        from internships.models import Internship
        from applications.models import Application
        from evaluations.models import Evaluation
        
        total_students = User.objects.filter(role='student').count()
        placed_students = Internship.objects.filter(
            status__in=['ongoing', 'completed']
        ).values('student').distinct().count()
        
        apps_pending = Application.objects.filter(status='pending').count()
        apps_accepted = Application.objects.filter(status='accepted').count()
        apps_rejected = Application.objects.filter(status='rejected').count()
        total_apps = apps_pending + apps_accepted + apps_rejected or 1
        
        avg_grade = Evaluation.objects.filter(
            is_validated=True
        ).aggregate(avg=Avg('final_grade'))['avg'] or 0
        
        by_level = list(StudentProfile.objects.values('niveau_etude').annotate(count=Count('id')))
        
        return Response({
            'totalStudents': total_students,
            'placedStudents': placed_students,
            'placementRate': round(placed_students / max(total_students, 1) * 100),
            'averageGrade': f'{avg_grade:.1f}',
            'byLevel': [{'name': l['niveau_etude'] or 'Unknown', 'count': l['count']} for l in by_level],
            'appsByStatus': [
                {'name': 'Pending', 'count': apps_pending, 'percent': round(apps_pending/total_apps*100), 'color': 'bg-amber-500'},
                {'name': 'Accepted', 'count': apps_accepted, 'percent': round(apps_accepted/total_apps*100), 'color': 'bg-green-500'},
                {'name': 'Rejected', 'count': apps_rejected, 'percent': round(apps_rejected/total_apps*100), 'color': 'bg-red-500'},
            ],
            'topHospitals': []
        })



class ConversationListView(generics.ListCreateAPIView):
    """List user's conversations"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class ConversationMessagesView(APIView):
    """Get/send messages in a conversation"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = conversation.messages.all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response(serializer.data)
    
    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=request.data.get('content', '')
        )
        conversation.save()
        return Response(MessageSerializer(message).data, status=201)



@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def toggle_user_active(request, pk):
    """Toggle user active status (admin only)"""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Not authorized'}, status=403)
    
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return Response({'is_active': user.is_active})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reset_user_password(request, pk):
    """Send password reset email (admin only)"""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Not authorized'}, status=403)
    
    user = get_object_or_404(User, pk=pk)
    return Response({'detail': 'Password reset email sent'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_profile(request):
    """Mark student profile as completed"""
    profile = get_object_or_404(StudentProfile, user=request.user)
    profile.profile_completed = True
    profile.save()
    return Response({"message": "Profile marked as completed"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_health(request):
    """Check if student profile is complete"""
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    required_fields = ['student_number', 'niveau_etude', 'specialite', 'faculty', 'university', 'phone']
    missing_fields = [field for field in required_fields if not getattr(profile, field)]
    has_documents = profile.documents.exists()
    
    return Response({
        "profile_completed": profile.profile_completed,
        "missing_fields": missing_fields,
        "has_documents": has_documents,
        "is_complete": len(missing_fields) == 0 and has_documents
    })