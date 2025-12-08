"""
Enhanced calendar export with subscription URLs and external calendar integration.
"""
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from datetime import timedelta
import hashlib
from .models import Internship
from internships.models import Schedule


def generate_calendar_token(user):
    """Generate a unique token for calendar subscription."""
    data = f"{user.id}:{user.email}:{user.date_joined.isoformat()}"
    return hashlib.sha256(data.encode()).hexdigest()[:32]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_calendar_links(request):
    """Get calendar subscription and integration links."""
    user = request.user
    token = generate_calendar_token(user)
    base_url = request.build_absolute_uri('/')[:-1]
    
    ical_sub_url = f"{base_url}/api/internships/calendar/subscribe/{token}/"
    
    google_add_url = f"https://calendar.google.com/calendar/render?cid={ical_sub_url.replace('https://', 'webcal://').replace('http://', 'webcal://')}"
    
    outlook_url = f"https://outlook.live.com/owa/?path=/calendar/action/compose&rru=addsubscription&url={ical_sub_url}&name=MedIntern"
    
    return Response({
        'ical_subscription': ical_sub_url,
        'webcal_url': ical_sub_url.replace('https://', 'webcal://').replace('http://', 'webcal://'),
        'google_calendar': google_add_url,
        'outlook': outlook_url,
        'one_time_download': f"{base_url}/api/internships/schedule/export/",
        'instructions': {
            'google': 'Click the Google Calendar link or paste the iCal URL in Google Calendar settings > Add other calendar > From URL',
            'outlook': 'Click the Outlook link or paste the iCal URL in Outlook > Add calendar > Subscribe from web',
            'apple': 'Copy the webcal:// URL and paste in Calendar app > File > New Calendar Subscription',
            'general': 'Most calendar apps support subscribing via the iCal URL'
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def calendar_subscription(request, token):
    """
    Public endpoint for calendar subscriptions.
    Token authenticates the user without login.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = None
    for u in User.objects.filter(is_active=True):
        if generate_calendar_token(u) == token:
            user = u
            break
    
    if not user:
        return HttpResponse("Invalid subscription token", status=401)
    
    now = timezone.now()
    ical_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MedIntern//Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:MedIntern - {user.full_name}",
        "X-WR-TIMEZONE:UTC",
    ]
    
    events = Schedule.objects.filter(
        user=user,
        start_time__gte=now - timedelta(days=30)
    ).order_by('start_time')[:100]
    
    for event in events:
        start_dt = event.start_time
        end_dt = event.end_time or (start_dt + timedelta(hours=1))
        
        ical_content.extend([
            "BEGIN:VEVENT",
            f"UID:medintern-schedule-{event.id}@medintern",
            f"DTSTAMP:{now.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{event.title}",
            f"DESCRIPTION:{event.description or ''}",
            f"LOCATION:{event.location or ''}",
            "END:VEVENT",
        ])
    
    if user.role == 'student':
        internships = Internship.objects.filter(
            student__user=user,
            status='active'
        ).select_related('offer')
        
        for internship in internships:
            if internship.offer.start_date and internship.offer.end_date:
                ical_content.extend([
                    "BEGIN:VEVENT",
                    f"UID:medintern-internship-{internship.id}@medintern",
                    f"DTSTAMP:{now.strftime('%Y%m%dT%H%M%SZ')}",
                    f"DTSTART;VALUE=DATE:{internship.offer.start_date.strftime('%Y%m%d')}",
                    f"DTEND;VALUE=DATE:{internship.offer.end_date.strftime('%Y%m%d')}",
                    f"SUMMARY:Internship: {internship.offer.title}",
                    f"DESCRIPTION:Hospital: {internship.offer.hospital.name if internship.offer.hospital else 'N/A'}",
                    "END:VEVENT",
                ])
    
    ical_content.append("END:VCALENDAR")
    
    response = HttpResponse("\r\n".join(ical_content), content_type='text/calendar')
    response['Content-Disposition'] = f'inline; filename="medintern_{user.id}.ics"'
    response['Cache-Control'] = 'public, max-age=3600'
    return response
