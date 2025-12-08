"""
API views for optimization reports.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .optimization_reports import (
    get_optimization_summary,
    get_hospital_performance,
    get_applications_trend,
    get_specialty_demand,
    get_score_distribution,
    get_faculty_comparison,
    generate_full_report
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def optimization_summary(request):
    """Get optimization summary metrics."""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Admin access required'}, status=403)
    return Response(get_optimization_summary())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hospital_performance(request):
    """Get hospital performance metrics."""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Admin access required'}, status=403)
    return Response(get_hospital_performance())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def applications_trend(request):
    """Get applications trend over time."""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Admin access required'}, status=403)
    days = int(request.query_params.get('days', 30))
    return Response(get_applications_trend(days))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def specialty_demand(request):
    """Get specialty demand analysis."""
    if request.user.role not in ['faculty_admin', 'hospital_admin']:
        return Response({'detail': 'Admin access required'}, status=403)
    return Response(get_specialty_demand())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def full_optimization_report(request):
    """Get comprehensive optimization report."""
    if request.user.role != 'faculty_admin':
        return Response({'detail': 'Faculty admin access required'}, status=403)
    return Response(generate_full_report())
