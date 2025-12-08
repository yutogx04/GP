from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import InternshipOffer, Internship, InternshipJournal
from .serializers import (
    InternshipOfferListSerializer,
    InternshipOfferDetailSerializer,
    InternshipOfferCreateSerializer,
    InternshipSerializer
)


class InternshipOfferListView(generics.ListAPIView):
    """List all open internship offers (public)"""
    serializer_class = InternshipOfferListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = InternshipOffer.objects.filter(
            status='open',
            validation_status='approved'
        ).select_related('hospital', 'department')
        
        hospital = self.request.query_params.get('hospital')
        department = self.request.query_params.get('department')
        search = self.request.query_params.get('search')
        
        if hospital:
            queryset = queryset.filter(hospital_id=hospital)
        if department:
            queryset = queryset.filter(department_id=department)
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset


class AllOffersListView(generics.ListAPIView):
    """List all offers for faculty admin validation"""
    serializer_class = InternshipOfferListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'faculty_admin':
            return InternshipOffer.objects.none()
        return InternshipOffer.objects.all().select_related('hospital', 'department')


class InternshipOfferDetailView(generics.RetrieveAPIView):
    """Get single internship offer details"""
    serializer_class = InternshipOfferDetailSerializer
    permission_classes = [AllowAny]
    queryset = InternshipOffer.objects.all()


class InternshipOfferCreateView(generics.CreateAPIView):
    """Create new internship offer (Hospital Admin only)"""
    serializer_class = InternshipOfferCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class InternshipOfferUpdateView(generics.UpdateAPIView):
    """Update internship offer"""
    serializer_class = InternshipOfferCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return InternshipOffer.objects.filter(created_by=self.request.user)


class InternshipOfferDeleteView(generics.DestroyAPIView):
    """Delete internship offer"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return InternshipOffer.objects.filter(created_by=self.request.user)


class HospitalOffersView(generics.ListAPIView):
    """List offers for hospital admin's hospital"""
    serializer_class = InternshipOfferListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return InternshipOffer.objects.filter(
            created_by=self.request.user
        ).select_related('hospital', 'department')


class SupervisorInternshipsView(generics.ListAPIView):
    """List internships supervised by current user"""
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Internship.objects.filter(
            supervisor=self.request.user
        ).select_related('student__user', 'offer')


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def validate_offer(request, pk):
    """Faculty admin validates/rejects an offer"""
    if request.user.role != 'faculty_admin':
        return Response(
            {'detail': 'Only faculty admins can validate offers'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    offer = get_object_or_404(InternshipOffer, pk=pk)
    new_status = request.data.get('validation_status')
    
    if new_status not in ['approved', 'rejected']:
        return Response(
            {'detail': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    offer.validation_status = new_status
    if new_status == 'approved':
        offer.status = 'open'
    offer.save()
    
    return Response({'status': 'updated', 'validation_status': new_status})



from .models import Schedule
from .schedule_serializer import ScheduleSerializer
from django.http import HttpResponse
from datetime import datetime, timedelta


class ScheduleListCreateView(generics.ListCreateAPIView):
    """List and create schedule events"""
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Schedule.objects.filter(user=self.request.user)
        
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View, update, or delete a schedule event"""
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_calendar_ical(request):
    """Export user's calendar as iCal format"""
    schedules = Schedule.objects.filter(user=request.user)
    
    ical_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MedIntern//Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    
    for event in schedules:
        start_dt = datetime.combine(event.date, event.start_time)
        end_dt = datetime.combine(event.date, event.end_time)
        
        ical_content.extend([
            "BEGIN:VEVENT",
            f"UID:{event.id}@medintern",
            f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{event.title}",
            f"DESCRIPTION:{event.description}",
            f"LOCATION:{event.location}",
            "END:VEVENT",
        ])
    
    ical_content.append("END:VCALENDAR")
    
    response = HttpResponse("\r\n".join(ical_content), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="medintern_calendar.ics"'
    return response



from .import_export import (
    import_offers_csv, import_offers_json,
    export_offers_csv, export_offers_json,
    get_import_template_csv
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_offers(request):
    """
    Import internship offers from CSV or JSON file.
    Hospital admins only.
    """
    if request.user.role != 'hospital_admin':
        return Response(
            {'detail': 'Only hospital admins can import offers'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    from hospitals.models import HospitalAdmin
    try:
        hospital_admin = HospitalAdmin.objects.get(user=request.user)
        hospital = hospital_admin.hospital
    except HospitalAdmin.DoesNotExist:
        return Response(
            {'detail': 'Hospital not found for this user'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES.get('file')
    if not file:
        return Response(
            {'detail': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    filename = file.name.lower()
    content = file.read()
    
    if filename.endswith('.csv'):
        result = import_offers_csv(content, hospital, request.user)
    elif filename.endswith('.json'):
        result = import_offers_json(content, hospital, request.user)
    else:
        return Response(
            {'detail': 'Unsupported file format. Use CSV or JSON.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if result['errors']:
        return Response({
            'success': result['success'],
            'errors': result['errors'],
            'created_ids': result['created_ids']
        }, status=status.HTTP_400_BAD_REQUEST if result['success'] == 0 else status.HTTP_207_MULTI_STATUS)
    
    return Response({
        'success': result['success'],
        'created_ids': result['created_ids'],
        'message': f"Successfully imported {result['success']} offers"
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_offers(request):
    """
    Export internship offers to CSV or JSON.
    Hospital admins export their offers, faculty admins export all.
    """
    format_type = request.query_params.get('format', 'csv').lower()
    
    if request.user.role == 'hospital_admin':
        from hospitals.models import HospitalAdmin
        try:
            hospital_admin = HospitalAdmin.objects.get(user=request.user)
            queryset = InternshipOffer.objects.filter(
                hospital=hospital_admin.hospital
            ).select_related('hospital', 'department')
        except HospitalAdmin.DoesNotExist:
            return Response({'detail': 'Hospital not found'}, status=400)
    elif request.user.role == 'faculty_admin':
        queryset = InternshipOffer.objects.all().select_related('hospital', 'department')
    else:
        return Response(
            {'detail': 'Only hospital or faculty admins can export offers'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if format_type == 'json':
        content = export_offers_json(queryset)
        response = HttpResponse(content, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="offers.json"'
    else:
        content = export_offers_csv(queryset)
        response = HttpResponse(content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="offers.csv"'
    
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def import_template(request):
    """Get CSV template for importing offers."""
    content = get_import_template_csv()
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="import_template.csv"'
    return response



class StudentInternshipView(generics.ListAPIView):
    """List student's current internship(s)"""
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        from users.models import StudentProfile
        try:
            profile = StudentProfile.objects.get(user=self.request.user)
            return Internship.objects.filter(student=profile).select_related('offer', 'supervisor')
        except StudentProfile.DoesNotExist:
            return Internship.objects.none()


class JournalListCreateView(generics.ListCreateAPIView):
    """List and create journal entries for an internship"""
    from .serializers import InternshipJournalSerializer
    serializer_class = InternshipJournalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        internship_id = self.kwargs.get('internship_id')
        internship = get_object_or_404(Internship, pk=internship_id)
        
        user = self.request.user
        is_student = hasattr(user, 'student_profile') and internship.student == user.student_profile
        is_supervisor = internship.supervisor == user
        is_admin = user.role in ['hospital_admin', 'faculty_admin']
        
        if not (is_student or is_supervisor or is_admin):
            return InternshipJournal.objects.none()
        
        return internship.journal_entries.all().order_by('-date')
    
    def perform_create(self, serializer):
        internship_id = self.kwargs.get('internship_id')
        internship = get_object_or_404(Internship, pk=internship_id)
        
        user = self.request.user
        if not hasattr(user, 'student_profile') or internship.student != user.student_profile:
            raise PermissionDenied("Only the student can create journal entries")
        
        serializer.save(internship=internship)


class JournalDetailView(generics.RetrieveUpdateAPIView):
    """Get/update a specific journal entry"""
    from .serializers import InternshipJournalSerializer
    serializer_class = InternshipJournalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        internship_id = self.kwargs.get('internship_id')
        internship = get_object_or_404(Internship, pk=internship_id)
        
        user = self.request.user
        is_student = hasattr(user, 'student_profile') and internship.student == user.student_profile
        is_supervisor = internship.supervisor == user
        is_admin = user.role in ['hospital_admin', 'faculty_admin']
        
        if not (is_student or is_supervisor or is_admin):
            return InternshipJournal.objects.none()
        
        return internship.journal_entries.all()
    
    def perform_update(self, serializer):
        entry = self.get_object()
        internship = entry.internship
        user = self.request.user
        
        is_student = hasattr(user, 'student_profile') and internship.student == user.student_profile
        is_supervisor = internship.supervisor == user
        
        if is_supervisor:
            allowed_fields = ['supervisor_comments']
            for key in list(serializer.validated_data.keys()):
                if key not in allowed_fields:
                    del serializer.validated_data[key]
        
        serializer.save()


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_internship_status(request, pk):
    """Update internship status (start/complete)"""
    internship = get_object_or_404(Internship, pk=pk)
    
    user = request.user
    is_supervisor = internship.supervisor == user
    is_admin = user.role in ['hospital_admin', 'faculty_admin']
    
    if not (is_supervisor or is_admin):
        return Response(
            {'detail': 'Only supervisors or admins can update internship status'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    new_status = request.data.get('status')
    valid_transitions = {
        'pending': ['ongoing', 'cancelled'],
        'ongoing': ['completed', 'cancelled'],
        'completed': [],
        'cancelled': []
    }
    
    if new_status not in valid_transitions.get(internship.status, []):
        return Response(
            {'detail': f'Cannot transition from {internship.status} to {new_status}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    internship.status = new_status
    internship.save(update_fields=['status'])
    
    if new_status == 'completed':
        from evaluations.models import Evaluation
        Evaluation.objects.get_or_create(
            internship=internship,
            defaults={'supervisor': internship.supervisor}
        )
    
    return Response({
        'status': internship.status,
        'message': f'Internship status updated to {new_status}'
    })

