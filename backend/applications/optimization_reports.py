"""
Assignment optimization analytics and reports.
Provides insights into application matching and slot utilization.
"""
from django.db.models import Count, Avg, F, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from .models import Application
from internships.models import InternshipOffer, Internship


def get_optimization_summary():
    """Get overall optimization metrics."""
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    total_apps = Application.objects.count()
    recent_apps = Application.objects.filter(applied_at__gte=thirty_days_ago).count()
    
    status_breakdown = Application.objects.values('status').annotate(count=Count('id'))
    
    accepted = Application.objects.filter(status='accepted').count()
    acceptance_rate = (accepted / total_apps * 100) if total_apps > 0 else 0
    
    reviewed_apps = Application.objects.filter(
        reviewed_at__isnull=False,
        applied_at__isnull=False
    )
    
    avg_review_time = None
    if reviewed_apps.exists():
        total_hours = sum([
            (app.reviewed_at - app.applied_at).total_seconds() / 3600
            for app in reviewed_apps[:100]  # Sample for performance
        ])
        avg_review_time = total_hours / min(reviewed_apps.count(), 100)
    
    total_slots = InternshipOffer.objects.filter(status='open').aggregate(
        total=Count('slots')
    )['total'] or 0
    filled_slots = Internship.objects.filter(status='active').count()
    utilization_rate = (filled_slots / total_slots * 100) if total_slots > 0 else 0
    
    return {
        'total_applications': total_apps,
        'recent_applications': recent_apps,
        'status_breakdown': {item['status']: item['count'] for item in status_breakdown},
        'acceptance_rate': round(acceptance_rate, 1),
        'avg_review_time_hours': round(avg_review_time, 1) if avg_review_time else None,
        'total_slots': total_slots,
        'filled_slots': filled_slots,
        'utilization_rate': round(utilization_rate, 1),
        'generated_at': now.isoformat()
    }


def get_hospital_performance():
    """Get performance metrics by hospital."""
    hospitals = Application.objects.values(
        'offer__hospital__id',
        'offer__hospital__name'
    ).annotate(
        total_apps=Count('id'),
        accepted=Count('id', filter=Q(status='accepted')),
        rejected=Count('id', filter=Q(status='rejected')),
        pending=Count('id', filter=Q(status='pending'))
    ).order_by('-total_apps')[:20]
    
    result = []
    for h in hospitals:
        acceptance_rate = (h['accepted'] / h['total_apps'] * 100) if h['total_apps'] > 0 else 0
        result.append({
            'hospital_id': h['offer__hospital__id'],
            'hospital_name': h['offer__hospital__name'],
            'total_applications': h['total_apps'],
            'accepted': h['accepted'],
            'rejected': h['rejected'],
            'pending': h['pending'],
            'acceptance_rate': round(acceptance_rate, 1)
        })
    
    return result


def get_applications_trend(days=30):
    """Get application trend over time."""
    since = timezone.now() - timedelta(days=days)
    
    daily = Application.objects.filter(
        applied_at__gte=since
    ).annotate(
        date=TruncDate('applied_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    return [{'date': item['date'].isoformat(), 'count': item['count']} for item in daily]


def get_specialty_demand():
    """Analyze demand by specialty."""
    specialties = Application.objects.values(
        'offer__specialty'
    ).annotate(
        demand=Count('id')
    ).order_by('-demand')[:15]
    
    return [
        {'specialty': s['offer__specialty'] or 'Unspecified', 'applications': s['demand']}
        for s in specialties
    ]


def get_score_distribution():
    """Analyze application score distribution."""
    ranges = [
        ('0-5', 0, 5),
        ('5-10', 5, 10),
        ('10-15', 10, 15),
        ('15-20', 15, 20),
        ('20+', 20, 100)
    ]
    
    distribution = []
    for label, min_score, max_score in ranges:
        count = Application.objects.filter(
            score__gte=min_score,
            score__lt=max_score
        ).count()
        distribution.append({'range': label, 'count': count})
    
    return distribution


def get_faculty_comparison():
    """Compare performance across faculties (if multiple exist)."""
    faculties = Application.objects.values(
        'student__student_profile__faculty'
    ).annotate(
        total=Count('id'),
        accepted=Count('id', filter=Q(status='accepted')),
        avg_score=Avg('score')
    ).order_by('-total')
    
    return [
        {
            'faculty': f['student__student_profile__faculty'] or 'Unknown',
            'total_applications': f['total'],
            'accepted': f['accepted'],
            'avg_score': round(f['avg_score'] or 0, 2),
            'placement_rate': round((f['accepted'] / f['total'] * 100) if f['total'] > 0 else 0, 1)
        }
        for f in faculties
    ]


def generate_full_report():
    """Generate comprehensive optimization report."""
    return {
        'summary': get_optimization_summary(),
        'hospital_performance': get_hospital_performance(),
        'applications_trend': get_applications_trend(),
        'specialty_demand': get_specialty_demand(),
        'score_distribution': get_score_distribution(),
        'faculty_comparison': get_faculty_comparison()
    }
