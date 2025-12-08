"""
Celery tasks for sending reminder notifications.
"""
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def send_schedule_reminders():
    """
    Check for upcoming events and send reminders.
    Should be called periodically (e.g., every 15 minutes).
    """
    from internships.models import Schedule
    from .email_service import send_reminder_email
    from .models import Notification
    
    now = timezone.now()
    today = now.date()
    current_time = now.time()
    
    one_hour_later = (now + timedelta(hours=1)).time()
    
    upcoming_1h = Schedule.objects.filter(
        date=today,
        start_time__lte=one_hour_later,
        start_time__gt=current_time,
        reminder_1h=True,
        reminder_sent_1h=False
    )
    
    for event in upcoming_1h:
        try:
            send_reminder_email(
                user=event.user,
                event_title=event.title,
                event_date=event.date.strftime('%B %d, %Y'),
                event_time=event.start_time.strftime('%H:%M'),
                event_location=event.location,
                event_description=event.description
            )
            
            Notification.objects.create(
                recipient=event.user,
                notification_type='reminder',
                title=f'Starting soon: {event.title}',
                message=f'Your event "{event.title}" starts at {event.start_time.strftime("%H:%M")}',
                link='/calendar'
            )
            
            event.reminder_sent_1h = True
            event.save(update_fields=['reminder_sent_1h'])
            
            logger.info(f'1h reminder sent for event {event.id} to {event.user.email}')
            
        except Exception as e:
            logger.error(f'Failed to send reminder for event {event.id}: {str(e)}')
    
    tomorrow = today + timedelta(days=1)
    upcoming_24h = Schedule.objects.filter(
        date=tomorrow,
        reminder_24h=True,
        reminder_sent_24h=False
    )
    
    for event in upcoming_24h:
        try:
            send_reminder_email(
                user=event.user,
                event_title=event.title,
                event_date=event.date.strftime('%B %d, %Y'),
                event_time=event.start_time.strftime('%H:%M'),
                event_location=event.location,
                event_description=event.description
            )
            
            Notification.objects.create(
                recipient=event.user,
                notification_type='reminder',
                title=f'Tomorrow: {event.title}',
                message=f'Your event "{event.title}" is scheduled for tomorrow at {event.start_time.strftime("%H:%M")}',
                link='/calendar'
            )
            
            event.reminder_sent_24h = True
            event.save(update_fields=['reminder_sent_24h'])
            
            logger.info(f'24h reminder sent for event {event.id} to {event.user.email}')
            
        except Exception as e:
            logger.error(f'Failed to send reminder for event {event.id}: {str(e)}')
    
    return {
        'reminders_1h': upcoming_1h.count(),
        'reminders_24h': upcoming_24h.count()
    }


try:
    from celery import shared_task
    
    @shared_task
    def send_reminders_task():
        """Celery task to send schedule reminders."""
        return send_schedule_reminders()
        
except ImportError:
    pass
