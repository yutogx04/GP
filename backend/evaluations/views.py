from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Evaluation, AutoEvaluation
from .serializers import (
    EvaluationListSerializer,
    EvaluationDetailSerializer,
    EvaluationCreateSerializer
)


class EvaluationListView(generics.ListAPIView):
    """List all evaluations (admin view)"""
    serializer_class = EvaluationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['faculty_admin', 'hospital_admin']:
            return Evaluation.objects.all().select_related(
                'internship__student__user',
                'internship__offer',
                'supervisor'
            )
        return Evaluation.objects.none()


class StudentEvaluationsView(generics.ListAPIView):
    """List student's own evaluations"""
    serializer_class = EvaluationDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Evaluation.objects.filter(
            internship__student__user=self.request.user,
            is_validated=True
        ).select_related('internship__offer__hospital', 'supervisor')


class SupervisorEvaluationsView(generics.ListAPIView):
    """List evaluations by supervisor"""
    serializer_class = EvaluationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Evaluation.objects.filter(
            supervisor=self.request.user
        ).select_related('internship__student__user', 'internship__offer')


class EvaluationDetailView(generics.RetrieveAPIView):
    """Get evaluation details"""
    serializer_class = EvaluationDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Evaluation.objects.all()


class EvaluationCreateView(generics.CreateAPIView):
    """Create new evaluation (Supervisor only)"""
    serializer_class = EvaluationCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(supervisor=self.request.user)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def validate_evaluation(request, pk):
    """Faculty admin validates an evaluation"""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response(
            {'detail': 'Only admins can validate evaluations'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    evaluation = get_object_or_404(Evaluation, pk=pk)
    
    evaluation.is_validated = True
    evaluation.validated_by = request.user
    evaluation.validation_date = timezone.now()
    evaluation.admin_signature = True
    evaluation.save()
    
    return Response({'status': 'Evaluation validated'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_evaluation_pdf(request, pk):
    """Download evaluation as PDF"""
    evaluation = get_object_or_404(Evaluation, pk=pk)
    
    user = request.user
    is_student = hasattr(user, 'student_profile') and evaluation.internship.student == user.student_profile
    is_supervisor = evaluation.supervisor == user
    is_admin = user.role in ['faculty_admin', 'hospital_admin']
    
    if not (is_student or is_supervisor or is_admin):
        return Response(
            {'detail': 'You do not have permission to download this evaluation'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    from .pdf_service import generate_evaluation_pdf
    return generate_evaluation_pdf(evaluation)

