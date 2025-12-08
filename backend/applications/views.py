from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Application, ApplicationDocument
from .serializers import (
    ApplicationListSerializer,
    ApplicationDetailSerializer,
    ApplicationCreateSerializer
)


class ApplicationListView(generics.ListAPIView):
    """List student's own applications"""
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.filter(
            student=self.request.user
        ).select_related('offer__hospital', 'offer__department')


class HospitalApplicationsView(generics.ListAPIView):
    """List applications for hospital admin's offers"""
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'hospital_admin':
            return Application.objects.none()
        return Application.objects.filter(
            offer__created_by=self.request.user
        ).select_related('student', 'offer')


class ApplicationDetailView(generics.RetrieveAPIView):
    """Get application details"""
    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Application.objects.filter(student=user)
        elif user.role == 'hospital_admin':
            return Application.objects.filter(offer__created_by=user)
        return Application.objects.none()


class ApplicationCreateView(generics.CreateAPIView):
    """Submit new application"""
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ApplicationUpdateView(generics.UpdateAPIView):
    """Update application status (Hospital Admin)"""
    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'hospital_admin':
            return Application.objects.none()
        return Application.objects.filter(offer__created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user,
            reviewed_at=timezone.now()
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_application(request, pk):
    """Student withdraws their application"""
    application = get_object_or_404(Application, pk=pk, student=request.user)
    
    if application.status not in ['pending', 'reviewing']:
        return Response(
            {'detail': 'Cannot withdraw application with current status'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    application.status = 'withdrawn'
    application.save()
    
    return Response({'status': 'Application withdrawn'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_assignment_scores(request):
    """Calculate scores for automatic assignment (Faculty Admin)"""
    if request.user.role != 'faculty_admin':
        return Response(
            {'detail': 'Only faculty admins can calculate scores'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    applications = Application.objects.filter(status='pending').select_related('student__student_profile')
    
    updated = 0
    for app in applications:
        try:
            profile = app.student.student_profile
            gpa = profile.average_grade or 10  # Default to 10 if no GPA
            priority_bonus = (4 - (app.priority or 3)) * 2  # Priority 1 = +6, Priority 2 = +4, Priority 3 = +2
            app.score = gpa + priority_bonus
            app.save(update_fields=['score'])
            updated += 1
        except Exception:
            continue
    
    return Response({'updated': updated})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def bulk_update_status(request):
    """
    Bulk update application statuses for drag-drop assignment board.
    
    Request body:
    {
        "updates": [
            {"id": 1, "status": "accepted"},
            {"id": 2, "status": "rejected"},
        ]
    }
    """
    if request.user.role not in ['hospital_admin', 'faculty_admin']:
        return Response(
            {'detail': 'Only hospital or faculty admins can update application statuses'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    updates = request.data.get('updates', [])
    if not updates:
        return Response({'detail': 'No updates provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_statuses = ['pending', 'reviewing', 'accepted', 'rejected', 'withdrawn']
    results = {'updated': 0, 'errors': []}
    
    for update in updates:
        app_id = update.get('id')
        new_status = update.get('status')
        
        if not app_id or not new_status:
            results['errors'].append(f'Invalid update: {update}')
            continue
        
        if new_status not in valid_statuses:
            results['errors'].append(f'Invalid status for app {app_id}: {new_status}')
            continue
        
        try:
            if request.user.role == 'hospital_admin':
                app = Application.objects.get(id=app_id, offer__created_by=request.user)
            else:
                app = Application.objects.get(id=app_id)
            
            old_status = app.status
            app.status = new_status
            
            if old_status == 'pending' and new_status in ['reviewing', 'accepted', 'rejected']:
                app.reviewed_at = timezone.now()
            
            app.save()
            results['updated'] += 1
            
            
        except Application.DoesNotExist:
            results['errors'].append(f'Application {app_id} not found or not accessible')
        except Exception as e:
            results['errors'].append(f'Error updating {app_id}: {str(e)}')
    
    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assignment_board_data(request):
    """
    Get all applications grouped by status for Kanban board.
    Hospital admins see their offers, faculty admins see all.
    """
    if request.user.role not in ['hospital_admin', 'faculty_admin']:
        return Response(
            {'detail': 'Only admins can access assignment board'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.user.role == 'hospital_admin':
        applications = Application.objects.filter(
            offer__created_by=request.user
        ).select_related('student', 'offer', 'offer__hospital')
    else:
        applications = Application.objects.all().select_related('student', 'offer', 'offer__hospital')
    
    grouped = {
        'pending': [],
        'reviewing': [],
        'accepted': [],
        'rejected': []
    }
    
    for app in applications:
        status_key = app.status if app.status in grouped else 'pending'
        grouped[status_key].append({
            'id': app.id,
            'student_name': app.student.full_name,
            'student_email': app.student.email,
            'offer_title': app.offer.title,
            'offer_id': app.offer.id,
            'hospital': app.offer.hospital.name if app.offer.hospital else None,
            'priority': app.priority,
            'score': app.score,
            'applied_at': app.applied_at.isoformat() if app.applied_at else None,
            'status': app.status
        })
    
    for status_key in grouped:
        grouped[status_key].sort(key=lambda x: (x['score'] or 0), reverse=True)
    
    return Response(grouped)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_application(request, pk):
    """
    Accept an application and create an internship with supervisor assignment.
    Hospital Admin only.
    
    Request body:
    {
        "supervisor_id": <int>  # Required - the encadrant to assign
    }
    """
    from internships.models import Internship, InternshipOffer
    from users.models import StudentProfile
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    if request.user.role != 'hospital_admin':
        return Response(
            {'detail': 'Only hospital admins can accept applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    application = get_object_or_404(
        Application, 
        pk=pk, 
        offer__created_by=request.user
    )
    
    if application.status == 'accepted':
        return Response(
            {'detail': 'Application already accepted'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    supervisor_id = request.data.get('supervisor_id')
    if not supervisor_id:
        return Response(
            {'detail': 'supervisor_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        supervisor = User.objects.get(id=supervisor_id, role='encadrant')
    except User.DoesNotExist:
        return Response(
            {'detail': 'Invalid supervisor. Must be an encadrant.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    offer = application.offer
    if offer.available_slots <= 0:
        return Response(
            {'detail': 'No available slots for this offer'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    student_profile, _ = StudentProfile.objects.get_or_create(user=application.student)
    
    try:
        internship = Internship.objects.create(
            offer=offer,
            student=student_profile,
            supervisor=supervisor,
            start_date=offer.start_date,
            end_date=offer.end_date,
            status='pending'  # Will become 'ongoing' when internship starts
        )
    except Exception as e:
        return Response(
            {'detail': f'Failed to create internship: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    application.status = 'accepted'
    application.reviewed_by = request.user
    application.reviewed_at = timezone.now()
    application.save()
    
    offer.available_slots -= 1
    offer.save(update_fields=['available_slots'])
    
    
    return Response({
        'status': 'Application accepted',
        'internship_id': internship.id,
        'supervisor': supervisor.full_name,
        'student': application.student.full_name
    })
