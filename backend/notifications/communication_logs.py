"""
Communication audit logging system.
Tracks all messages and notifications for compliance and auditing.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class CommunicationLog(models.Model):
    """Audit log for all platform communications."""
    
    CHANNEL_TYPES = [
        ('email', 'Email'),
        ('in_app', 'In-App Notification'),
        ('message', 'Direct Message'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    DIRECTION_TYPES = [
        ('outbound', 'Outbound (System to User)'),
        ('inbound', 'Inbound (User to System)'),
        ('internal', 'Internal (User to User)'),
    ]
    
    STATUS_TYPES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    
    channel = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    direction = models.CharField(max_length=20, choices=DIRECTION_TYPES, default='outbound')
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_communications'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_communications'
    )
    recipient_email = models.EmailField(blank=True, help_text="For external recipients")
    
    subject = models.CharField(max_length=255, blank=True)
    content_preview = models.TextField(max_length=500, blank=True, help_text="First 500 chars")
    
    related_application = models.ForeignKey(
        'applications.Application',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    related_evaluation = models.ForeignKey(
        'evaluations.Evaluation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    related_message = models.ForeignKey(
        'users.Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='pending')
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    template_used = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['channel', 'status']),
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.channel} to {self.recipient or self.recipient_email} - {self.status}"
    
    def mark_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])
    
    def mark_delivered(self):
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save(update_fields=['status', 'delivered_at'])
    
    def mark_read(self):
        self.status = 'read'
        self.read_at = timezone.now()
        self.save(update_fields=['status', 'read_at'])
    
    def mark_failed(self, error_message=''):
        self.status = 'failed'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])
    
    @classmethod
    def log_email(cls, recipient, subject, content, sender=None, template=None, status='sent'):
        """Log an outbound email."""
        return cls.objects.create(
            channel='email',
            direction='outbound',
            sender=sender,
            recipient=recipient if hasattr(recipient, 'email') else None,
            recipient_email=recipient.email if hasattr(recipient, 'email') else str(recipient),
            subject=subject,
            content_preview=content[:500] if content else '',
            status=status,
            sent_at=timezone.now() if status == 'sent' else None,
            template_used=template or ''
        )
    
    @classmethod
    def log_notification(cls, recipient, content, sender=None):
        """Log an in-app notification."""
        return cls.objects.create(
            channel='in_app',
            direction='outbound',
            sender=sender,
            recipient=recipient,
            content_preview=content[:500],
            status='delivered',
            delivered_at=timezone.now()
        )
    
    @classmethod
    def log_message(cls, sender, recipient, content, message_obj=None):
        """Log a direct message between users."""
        return cls.objects.create(
            channel='message',
            direction='internal',
            sender=sender,
            recipient=recipient,
            content_preview=content[:500],
            related_message=message_obj,
            status='delivered',
            delivered_at=timezone.now()
        )
