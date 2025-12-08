"""
Centralized email service for MedIntern platform.
Sends HTML emails using Django's email backend.
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging

logger = logging.getLogger(__name__)

FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')


def send_templated_email(to_email, subject, template_name, context):
    """
    Send an HTML email using a template.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        template_name: Name of template in templates/emails/ (without .html)
        context: Context dictionary for template rendering
    """
    try:
        context['frontend_url'] = FRONTEND_URL
        
        html_content = render_to_string(f'emails/{template_name}.html', context)
        
        from django.utils.html import strip_tags
        text_content = strip_tags(html_content)
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@medintern.com')
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f"Email sent successfully to {to_email}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def send_verification_email(user, verification_url):
    """Send email verification email to new user."""
    return send_templated_email(
        to_email=user.email,
        subject="Verify Your Email - MedIntern",
        template_name="verification",
        context={
            'user': user,
            'verification_url': verification_url,
        }
    )


def send_password_reset_email(user):
    """Send password reset email with token."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{FRONTEND_URL}/reset-password?uid={uid}&token={token}"
    
    return send_templated_email(
        to_email=user.email,
        subject="Reset Your Password - MedIntern",
        template_name="password_reset",
        context={
            'user': user,
            'reset_url': reset_url,
        }
    )


def send_application_status_email(application):
    """Send application status update email."""
    return send_templated_email(
        to_email=application.student.email,
        subject=f"Application Update: {application.offer.title} - MedIntern",
        template_name="application_status",
        context={
            'user': application.student,
            'application': application,
        }
    )


def send_notification_email(notification):
    """Send general notification as email."""
    return send_templated_email(
        to_email=notification.recipient.email,
        subject=f"{notification.title} - MedIntern",
        template_name="notification",
        context={
            'user': notification.recipient,
            'notification': notification,
        }
    )


def send_reminder_email(user, event_title, event_date, event_time, event_location=None, event_description=None):
    """Send reminder email for upcoming event."""
    return send_templated_email(
        to_email=user.email,
        subject=f"Reminder: {event_title} - MedIntern",
        template_name="reminder",
        context={
            'user': user,
            'event_title': event_title,
            'event_date': event_date,
            'event_time': event_time,
            'event_location': event_location,
            'event_description': event_description,
        }
    )


def send_new_assignment_email(internship):
    """Notify supervisor about new student assignment."""
    if not internship.supervisor:
        return False
        
    return send_templated_email(
        to_email=internship.supervisor.email,
        subject=f"New Student Assignment - MedIntern",
        template_name="notification",
        context={
            'user': internship.supervisor,
            'notification': {
                'title': 'New Student Assigned',
                'message': f'{internship.student.user.full_name} has been assigned to your supervision for {internship.offer.title}.',
                'link': '/students',
            },
        }
    )
