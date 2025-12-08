"""
API endpoints for digital signature management.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Evaluation
from .signature_model import Signature


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_signature(request, evaluation_id):
    """
    Add a digital signature to an evaluation.
    
    Request body:
    {
        "signature_data": "data:image/png;base64,...",
        "signer_type": "supervisor" | "student" | "admin"
    }
    """
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    signature_data = request.data.get('signature_data')
    signer_type = request.data.get('signer_type')
    
    if not signature_data:
        return Response({'detail': 'Signature data is required'}, status=400)
    
    if signer_type not in ['supervisor', 'student', 'admin']:
        return Response({'detail': 'Invalid signer type'}, status=400)
    
    user = request.user
    if signer_type == 'supervisor' and user != evaluation.supervisor:
        return Response({'detail': 'Only the supervisor can sign as supervisor'}, status=403)
    if signer_type == 'student' and user != evaluation.internship.student.user:
        return Response({'detail': 'Only the student can sign as student'}, status=403)
    if signer_type == 'admin' and user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Only admins can sign as admin'}, status=403)
    
    signature, created = Signature.objects.update_or_create(
        evaluation=evaluation,
        signer_type=signer_type,
        defaults={
            'signer': user,
            'signature_data': signature_data,
            'signed_at': timezone.now(),
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500]
        }
    )
    
    return Response({
        'id': signature.id,
        'signer_type': signature.signer_type,
        'signed_at': signature.signed_at.isoformat(),
        'created': created
    }, status=201 if created else 200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_signatures(request, evaluation_id):
    """Get all signatures for an evaluation."""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    
    signatures = Signature.objects.filter(evaluation=evaluation)
    
    return Response([{
        'id': sig.id,
        'signer_type': sig.signer_type,
        'signer_name': sig.signer.full_name,
        'signed_at': sig.signed_at.isoformat(),
        'has_signature': bool(sig.signature_data)
    } for sig in signatures])


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_signature(request, evaluation_id, signer_type):
    """Delete a signature (only by the signer or admin)."""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    signature = get_object_or_404(Signature, evaluation=evaluation, signer_type=signer_type)
    
    user = request.user
    if user != signature.signer and user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Cannot delete this signature'}, status=403)
    
    signature.delete()
    return Response({'detail': 'Signature deleted'})


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
